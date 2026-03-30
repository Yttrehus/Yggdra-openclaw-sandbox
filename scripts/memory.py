#!/usr/bin/env python3
"""
Yggdra Memory Architecture v1.1
To collections: knowledge (hvad vi ved) + episodes (hvad der skete).
Hybrid search (dense + sparse), temporal decay, content hashing.
Nu med Dynamic RAG (adaptive retrieval windows).

Brug:
    python scripts/memory.py setup                    # Opret collections fra scratch
    python scripts/memory.py ingest <fil/mappe>       # Ingest markdown-filer
    python scripts/memory.py search "query"            # Søg med hybrid search + decay
    python scripts/memory.py status                    # Vis collection-stats
    python scripts/memory.py nuke                      # Slet knowledge + episodes
"""

import os
import sys
import json
import hashlib
import argparse
import uuid
import math
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, SparseVectorParams, SparseIndexParams,
    PointStruct, SparseVector, NamedVector, NamedSparseVector,
    Prefetch, FusionQuery, Fusion, SearchParams,
    models,
)
from openai import OpenAI

# --- Config ---

QDRANT_URL = "http://localhost:6333"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
CHUNK_SIZE = 800  # tokens (ca. 3200 chars)
CHUNK_OVERLAP = 100  # tokens overlap

COLLECTIONS = {
    "knowledge": "Alt vi ved: research, docs, etableret viden, projektbeskrivelser",
    "episodes": "Alt der skete: sessions, voice memos, beslutninger, handlinger",
}

# --- Data model ---

@dataclass
class Doc:
    id: str              # source_prefix + hash
    source: str          # "markdown", "voice_memo", "session"
    source_file: str     # original filsti
    text: str            # chunk-tekst
    title: str           # fil-titel eller heading
    chunk_index: int     # chunk nr i filen
    created_at: str      # ISO datetime
    indexed_at: str      # ISO datetime
    content_hash: str    # SHA256 af text
    confidence: str      # "established", "research", "draft", "unknown"
    references: list     # kilder hvis tilgængelige


# --- Sparse vector (BM25-approksimation) ---

def text_to_sparse(text: str) -> dict:
    """Simpel term-frequency sparse vector til BM25-approksimation."""
    words = text.lower().split()
    # Fjern korte ord og stop words
    stop = {"og", "i", "er", "en", "et", "den", "det", "de", "at", "på", "til",
            "med", "for", "af", "som", "kan", "har", "fra", "the", "a", "an",
            "is", "in", "to", "of", "and", "that", "it", "be", "was", "are"}
    words = [w for w in words if len(w) > 2 and w not in stop]

    # Term frequency
    tf = {}
    for w in words:
        h = hash(w) % 50000  # Hash til fast indeks-rum
        tf[h] = tf.get(h, 0) + 1

    if not tf:
        return {"indices": [0], "values": [0.1]}

    # Normaliser
    max_tf = max(tf.values())
    return {
        "indices": list(tf.keys()),
        "values": [v / max_tf for v in tf.values()],
    }


# --- Chunking ---

def chunk_markdown(text: str, source_file: str, max_chars: int = 2400, overlap_chars: int = 400) -> list[dict]:
    """Chunk markdown med heading-awareness. Respekterer ## og ### grænser.
    For tekst uden newlines (f.eks. Whisper-output): splitter på sætninger."""
    # Hvis teksten har meget få newlines, split på sætninger først
    if text.count("\n") < len(text) / 2000:
        import re
        # Split på sætningsgrænser (. ! ? efterfulgt af mellemrum)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        lines = []
        current = ""
        for s in sentences:
            if len(current) + len(s) > 200:
                if current:
                    lines.append(current)
                current = s
            else:
                current = f"{current} {s}".strip() if current else s
        if current:
            lines.append(current)
    else:
        lines = text.split("\n")
    chunks = []
    current_chunk = []
    current_heading = ""
    current_len = 0

    # Find titel (første # heading)
    title = Path(source_file).stem
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            title = line.lstrip("# ").strip()
            break

    for line in lines:
        # Ny heading = potentielt ny chunk
        if line.startswith("## ") or line.startswith("### "):
            if current_len > 200:  # Gem nuværende chunk hvis den har substans
                chunks.append({
                    "text": "\n".join(current_chunk),
                    "heading": current_heading,
                    "title": title,
                })
                # Overlap: behold sidste par linjer
                overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else []
                current_chunk = overlap_lines
                current_len = sum(len(l) for l in current_chunk)
            current_heading = line.lstrip("#").strip()

        current_chunk.append(line)
        current_len += len(line)

        # Hard split ved max_chars
        if current_len >= max_chars:
            chunks.append({
                "text": "\n".join(current_chunk),
                "heading": current_heading,
                "title": title,
            })
            overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else []
            current_chunk = overlap_lines
            current_len = sum(len(l) for l in current_chunk)

    # Sidste chunk
    if current_len > 50:
        chunks.append({
            "text": "\n".join(current_chunk),
            "heading": current_heading,
            "title": title,
        })

    return chunks


def detect_confidence(text: str, filepath: str) -> str:
    """Heuristisk confidence-detection baseret på indhold."""
    lower = text.lower()
    fp = filepath.lower()

    if "destillat" in fp or "deep_study" in fp:
        return "research"
    if "red_team" in fp or "evaluering" in fp:
        return "research"
    if any(w in lower for w in ["[solid]", "peer-reviewed", "replikeret"]):
        return "established"
    if any(w in lower for w in ["[vendor", "[anekdotisk", "draft", "udkast"]):
        return "draft"
    if any(w in lower for w in ["kilde:", "source:", "ref:", "reference"]):
        return "research"
    return "unknown"


def detect_collection(filepath: str) -> str:
    """Bestem collection baseret på filsti."""
    fp = filepath.lower()
    if any(w in fp for w in ["voice_memo", "session", "chatlog", "episode", "progress"]):
        return "episodes"
    return "knowledge"


# --- Core operations ---

def setup_collections(client: QdrantClient):
    """Opret knowledge og episodes med hybrid vector config."""
    for name, desc in COLLECTIONS.items():
        # Slet hvis den eksisterer
        try:
            client.delete_collection(name)
            print(f"  Slettet gammel '{name}'")
        except Exception:
            pass

        client.create_collection(
            collection_name=name,
            vectors_config={
                "dense": VectorParams(
                    size=EMBED_DIM,
                    distance=Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                "sparse": SparseVectorParams(
                    index=SparseIndexParams(on_disk=False),
                ),
            },
        )
        print(f"  Oprettet '{name}': {desc}")

    print("\nCollections klar. Hybrid search (dense + sparse) aktiveret.")


def embed_texts(openai_client: OpenAI, texts: list[str]) -> list[list[float]]:
    """Batch-embed tekster via OpenAI."""
    truncated = [t[:6000] for t in texts]
    all_embeddings = []
    for i in range(0, len(truncated), 20):
        batch = truncated[i:i+20]
        response = openai_client.embeddings.create(
            model=EMBED_MODEL,
            input=batch,
        )
        all_embeddings.extend([d.embedding for d in response.data])
    return all_embeddings


def ingest_file(filepath: str, client: QdrantClient, openai_client: OpenAI, force: bool = False) -> int:
    """Ingest én markdown-fil."""
    path = Path(filepath)
    if not path.exists():
        return 0
    if path.suffix.lower() not in {".md", ".txt"}:
        return 0

    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 100:
        return 0

    collection = detect_collection(filepath)
    confidence = detect_confidence(text, filepath)
    chunks = chunk_markdown(text, filepath)

    if not chunks:
        return 0

    chunk_texts = [c["text"] for c in chunks]
    enriched_texts = []
    for c in chunks:
        prefix = f"Dokument: {c['title']}"
        if c["heading"]:
            prefix += f" — {c['heading']}"
        enriched_texts.append(f"{prefix}\n\n{c['text']}")

    embeddings = embed_texts(openai_client, enriched_texts)

    points = []
    now = datetime.now(timezone.utc).isoformat()
    file_mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        content_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()[:16]
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"yggdra:{filepath}:{i}"))

        if not force:
            try:
                existing = client.retrieve(collection, [doc_id])
                if existing and existing[0].payload.get("content_hash") == content_hash:
                    continue
            except Exception:
                pass

        sparse = text_to_sparse(chunk["text"])

        point = PointStruct(
            id=doc_id,
            vector={
                "dense": embedding,
                "sparse": SparseVector(
                    indices=sparse["indices"],
                    values=sparse["values"],
                ),
            },
            payload={
                "source": "markdown",
                "source_file": str(path.name),
                "source_path": str(path),
                "title": chunk["title"],
                "heading": chunk["heading"],
                "text": chunk["text"],
                "chunk_index": i,
                "total_chunks": len(chunks),
                "created_at": file_mtime,
                "indexed_at": now,
                "content_hash": content_hash,
                "confidence": confidence,
                "collection": collection,
            },
        )
        points.append(point)

    if not points:
        return 0

    client.upsert(collection_name=collection, points=points)
    print(f"  {path.name} -> {collection}: {len(points)} chunks ({confidence})")
    return len(points)


def ingest_path(target: str, client: QdrantClient, openai_client: OpenAI, force: bool = False) -> int:
    """Ingest fil eller mappe."""
    path = Path(target)
    total = 0
    if path.is_file():
        total = ingest_file(str(path), client, openai_client, force)
    elif path.is_dir():
        md_files = sorted(path.rglob("*.md"))
        for f in md_files:
            if any(skip in str(f) for skip in [".git", "node_modules", "9_archive", "__pycache__"]):
                continue
            total += ingest_file(str(f), client, openai_client, force)
    return total


def calculate_dynamic_limit(query: str) -> int:
    """Beregner limit baseret på forespørgslens kompleksitet (Dynamic RAG)."""
    # Flere ord/tegn tyder på en kompleks forespørgsel, der kræver mere kontekst
    words = len(query.split())
    if words < 3: return 5   # Simpel forespørgsel
    if words < 8: return 10  # Medium
    return 20                # Kompleks

def search(query: str, client: QdrantClient, openai_client: OpenAI,
           collection: str = None, limit: int = None, decay_rate: float = 0.005) -> list:
    """Hybrid search med Dynamic RAG og Temporal Decay."""
    
    # 1. Dynamic Limit
    if limit is None:
        limit = calculate_dynamic_limit(query)
    
    # 2. Embed query
    query_embedding = embed_texts(openai_client, [query])[0]
    query_sparse = text_to_sparse(query)

    collections = [collection] if collection else ["knowledge", "episodes"]
    all_results = []

    for col in collections:
        try:
            # Hybrid search med RRF
            results = client.query_points(
                collection_name=col,
                prefetch=[
                    Prefetch(query=query_embedding, using="dense", limit=limit * 2),
                    Prefetch(query=SparseVector(indices=query_sparse["indices"], values=query_sparse["values"]), using="sparse", limit=limit * 2),
                ],
                query=FusionQuery(fusion=Fusion.RRF),
                limit=limit * 2,
            )

            for point in results.points:
                # 3. Temporal Decay (V6 Adaptive)
                created = point.payload.get("created_at", "")
                confidence = point.payload.get("confidence", "unknown")
                
                try:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    age_days = (datetime.now(timezone.utc) - created_dt).days
                    
                    # Evergreen protection: 'established' viden decay'er langsommere
                    current_decay_rate = decay_rate
                    if confidence == "established":
                        current_decay_rate *= 0.1 # 10x langsommere decay
                        
                    decay = 1 / (1 + math.log1p(age_days) * current_decay_rate * 10)
                except Exception:
                    decay = 0.5

                all_results.append({
                    "score": point.score * decay if point.score else decay,
                    "collection": col,
                    "title": point.payload.get("title", ""),
                    "heading": point.payload.get("heading", ""),
                    "source_file": point.payload.get("source_file", ""),
                    "confidence": confidence,
                    "created_at": created,
                    "text": point.payload.get("text", "")[:500],
                    "id": point.id,
                })
        except Exception as e:
            print(f"  Søgefejl i {col}: {e}")

    all_results.sort(key=lambda r: r["score"], reverse=True)
    return all_results[:limit]


def status(client: QdrantClient):
    """Vis status."""
    for col in client.get_collections().collections:
        info = client.get_collection(col.name)
        print(f"  {col.name}: {info.points_count} points")


def nuke(client: QdrantClient):
    """Slet knowledge + episodes."""
    for name in COLLECTIONS:
        try:
            client.delete_collection(name)
            print(f"  Slettet: {name}")
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Yggdra Memory Architecture v1.1")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("setup", help="Opret collections fra scratch")
    sub.add_parser("status", help="Vis collection-stats")
    sub.add_parser("nuke", help="Slet knowledge + episodes")

    p_ingest = sub.add_parser("ingest", help="Ingest markdown-filer")
    p_ingest.add_argument("path", help="Fil eller mappe")
    p_ingest.add_argument("--force", action="store_true", help="Re-ingest uændrede filer")

    p_search = sub.add_parser("search", help="Hybrid search med Dynamic RAG")
    p_search.add_argument("query", help="Søgestreng")
    p_search.add_argument("--collection", "-c", help="Søg kun i denne collection")
    p_search.add_argument("--limit", "-n", type=int, help="Overstyr dynamic limit")
    p_search.add_argument("--decay", type=float, default=0.005, help="Temporal decay rate")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = QdrantClient(url=QDRANT_URL, timeout=120)
    openai_client = OpenAI(api_key=OPENAI_KEY)

    if args.command == "setup":
        setup_collections(client)
    elif args.command == "status":
        status(client)
    elif args.command == "nuke":
        confirm = input("Slet knowledge + episodes? (ja/nej): ")
        if confirm.lower() == "ja":
            nuke(client)
    elif args.command == "ingest":
        ingest_path(args.path, client, openai_client, args.force)
    elif args.command == "search":
        results = search(args.query, client, openai_client,
                        collection=args.collection, limit=args.limit,
                        decay_rate=args.decay)
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r['title']} | Score: {r['score']:.4f}\n    {r['text'][:200]}...")

if __name__ == "__main__":
    main()
