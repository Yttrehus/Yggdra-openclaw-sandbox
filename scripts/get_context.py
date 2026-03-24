#!/usr/bin/env python3
"""
Context Retrieval v2.1 — Hybrid Search + Temporal Decay + Reranking

Henter relevant kontekst fra Qdrant med intelligent retrieval routing og post-processing:
1. Retrieval: Hybrid (Dense + Sparse) via Qdrant
2. Processing: Temporal Decay (Nedprioriterer gammel viden)
3. Protection: Evergreen Protection (Bevarer vision og principper)
4. Reranking: Semantisk Reranking via Cohere API (fallback til keyword boost)
"""

import sys
import re
import argparse
import json
import math
import os
from datetime import datetime, timezone, date
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue, MatchText,
    SparseVector, Prefetch, FusionQuery, Fusion
)

# Config — sti-uafhængig
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

def _load_openai_key():
    """Læs API key fra env var eller CREDENTIALS.md"""
    key = os.environ.get("OPENAI_API_KEY")
    if key: return key
    creds_path = os.path.join(_PROJECT_ROOT, "data", "CREDENTIALS.md")
    try:
        return open(creds_path).read().split('`')[1]
    except: return None

OPENAI_KEY = _load_openai_key()
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
COHERE_KEY = os.environ.get("COHERE_API_KEY")

# Clients
openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
qdrant = QdrantClient(url=QDRANT_URL)

# ─── Temporal Decay & Evergreen ──────────────────────────────────

HALFLIFE_DAYS = 30
DECAY_LAMBDA = math.log(2) / HALFLIFE_DAYS

EVERGREEN_PATTERNS = [
    "BLUEPRINT.md", "IDENTITY.md", "SOUL.md", "CLAUDE.md",
    "manuals/", "KNB.manuals/", "rules/", "SPEC-", "MISSION.md",
    "YGGDRA_SCAN.md", "PIPELINE_DESIGN.md"
]

def is_evergreen(payload):
    if payload.get('is_evergreen'): return True
    source = payload.get('source') or payload.get('file_path') or ""
    return any(p in source for p in EVERGREEN_PATTERNS)

def apply_decay(points, collection):
    """Anvender temporal decay på søgeresultater."""
    # Collections uden decay
    if collection in {"advisor_brain", "miessler_bible", "knowledge"}:
        return points

    now = datetime.now(timezone.utc)
    for p in points:
        if is_evergreen(p.payload):
            p.decay_factor = 1.0
            continue
            
        date_str = p.payload.get("date") or p.payload.get("created_at") or p.payload.get("timestamp")
        if not date_str:
            p.decay_factor = 1.0
            continue

        try:
            # ISO parsing robusthed
            ts = date_str.replace('Z', '+00:00')
            point_dt = datetime.fromisoformat(ts)
            if point_dt.tzinfo is None: point_dt = point_dt.replace(tzinfo=timezone.utc)
            
            age_days = (now - point_dt).total_seconds() / (24 * 3600)
            p.decay_factor = math.exp(-max(0, age_days) * DECAY_LAMBDA)
            p.score *= p.decay_factor
        except:
            p.decay_factor = 1.0

    return sorted(points, key=lambda x: x.score, reverse=True)

# ─── Reranking ────────────────────────────────────────────────────

def rerank_results(query, points, limit=5):
    """Reranker resultater for at sikre semantisk match."""
    if not points: return []
    
    # Forsøg Cohere Rerank hvis nøgle findes
    if COHERE_KEY:
        try:
            import requests
            docs = [p.payload.get('text', str(p.payload)) for p in points]
            resp = requests.post(
                "https://api.cohere.ai/v1/rerank",
                headers={"authorization": f"Bearer {COHERE_KEY}", "content-type": "application/json"},
                json={"model": "rerank-v3.0", "query": query, "documents": docs, "top_n": limit},
                timeout=5
            )
            if resp.status_code == 200:
                reranked = resp.json().get('results', [])
                final = []
                for r in reranked:
                    p = points[r['index']]
                    p.rerank_score = r['relevance_score']
                    final.append(p)
                return final
        except: pass

    # Fallback: Simpel keyword boost reranker
    for p in points:
        text = str(p.payload).lower()
        boost = 0.0
        # Fjern stopord og tegn fra query for bedre match
        query_terms = re.sub(r'[^\w\s]', '', query).lower().split()
        for word in query_terms:
            if len(word) > 3:
                # Kraftigere boost hvis hele ordet findes
                if word in text:
                    boost += 0.40
                # Lille boost hvis ordet findes delvist (stemming-ish)
                elif len(word) > 5 and word[:5] in text:
                    boost += 0.15
        p.rerank_score = min(1.0, p.score + boost)
        
    return sorted(points, key=lambda x: getattr(x, 'rerank_score', x.score), reverse=True)[:limit]

# ─── Core Retrieval ───────────────────────────────────────────────

def get_dense_embedding(text):
    if not openai_client: return [0.0] * 1536
    resp = openai_client.embeddings.create(model="text-embedding-3-small", input=[text])
    return resp.data[0].embedding

def get_sparse_embedding(text):
    try:
        from fastembed import SparseTextEmbedding
        model = SparseTextEmbedding(model_name='Qdrant/bm25')
        result = list(model.embed([text]))[0]
        return SparseVector(indices=result.indices.tolist(), values=result.values.tolist())
    except: return None

def search_hybrid(query, collection, limit=5, qdrant_filter=None):
    """Hybrid search: dense + sparse via RRF."""
    dense_vector = get_dense_embedding(query)
    sparse_vector = get_sparse_embedding(query)

    if not sparse_vector: # Fallback til dense hvis fastembed fejler
        results = qdrant.query_points(collection_name=collection, query=dense_vector, limit=limit*4, query_filter=qdrant_filter)
        points = results.points
    else:
        results = qdrant.query_points(
            collection_name=collection,
            prefetch=[
                Prefetch(query=dense_vector, using="dense", limit=limit*4, filter=qdrant_filter),
                Prefetch(query=sparse_vector, using="sparse", limit=limit*4, filter=qdrant_filter),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit * 4,
        )
        points = results.points

    # 1. Temporal Decay
    points = apply_decay(points, collection)
    
    # 2. Reranking
    points = rerank_results(query, points, limit)
    
    return points

# ─── Entry Point ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Yggdra Context Retrieval v2.1')
    parser.add_argument('query', help='Søgetekst')
    parser.add_argument('--limit', '-l', type=int, default=5)
    parser.add_argument('--collection', '-c', default='routes')
    args = parser.parse_args()

    points = search_hybrid(args.query, args.collection, limit=args.limit)
    
    if not points:
        print("Ingen relevante resultater fundet.")
        return

    print(f"--- Top {len(points)} resultater for: '{args.query}' ---\n")
    for p in points:
        score = getattr(p, 'rerank_score', p.score)
        evergreen = " [EVERGREEN]" if is_evergreen(p.payload) else ""
        print(f"[{score:.3f}]{evergreen} {p.payload.get('kunde', p.payload.get('fact', 'Uden titel'))}")
        print(f"  Kilde: {p.payload.get('source', p.payload.get('file_path', 'ukendt'))}")
        text = p.payload.get('text', p.payload.get('content', ''))
        if text: print(f"  Uddrag: {text[:150]}...")
        print("")

if __name__ == "__main__":
    main()
