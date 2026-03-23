#!/usr/bin/env python3
"""
Context Retrieval v2 — Hybrid Search + Pattern Matching + Metadata Filtering

Henter relevant kontekst fra Qdrant med intelligent retrieval routing:
- Semantic search (dense vectors) for naturligt sprog
- Keyword search (sparse vectors/BM25) for navne og adresser
- Hybrid search (dense + sparse via RRF) som default
- Metadata filtering for strukturerede queries (dato, ugedag, rute_id)
- Pattern matching (regex) for koder, IDs, telefonnumre

Brug:
  python3 get_context.py "hvor ligger McDonalds?"                    # Hybrid (default)
  python3 get_context.py "alle stops i Randers" --filter bynavn=Randers
  python3 get_context.py "mandagsruter december" --filter weekday=mandag,month=12
  python3 get_context.py "rutekode 256" --exact                      # Pattern match
  python3 get_context.py "rute 231" --filter rute_id_abs=231
  python3 get_context.py "hvad snakkede vi om?" --conversations
"""

import sys
import re
import argparse
import json
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue, MatchText, Range,
    SparseVector, NamedSparseVector, NamedVector,
    Prefetch, FusionQuery, Fusion, QueryRequest
)

# Config — sti-uafhængig (virker på VPS og lokalt PC)
import os
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

def _load_openai_key():
    """Læs API key fra env var eller CREDENTIALS.md"""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    creds_path = os.path.join(_PROJECT_ROOT, "data", "CREDENTIALS.md")
    return open(creds_path).read().split('`')[1]

OPENAI_KEY = _load_openai_key()
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
GLOSSARY_PATH = os.path.join(_PROJECT_ROOT, "data", "glossary.json")

# Clients
openai_client = OpenAI(api_key=OPENAI_KEY)
qdrant = QdrantClient(url=QDRANT_URL)

# Lazy-loaded models
_sparse_model = None
_reranker = None


def get_sparse_model():
    global _sparse_model
    if _sparse_model is None:
        from fastembed import SparseTextEmbedding
        _sparse_model = SparseTextEmbedding(model_name='Qdrant/bm25')
    return _sparse_model


def get_reranker():
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    return _reranker


def get_dense_embedding(text):
    """Dense embedding via OpenAI"""
    resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return resp.data[0].embedding


def get_sparse_embedding(text):
    """Sparse embedding via BM25"""
    model = get_sparse_model()
    result = list(model.embed([text]))[0]
    return SparseVector(
        indices=result.indices.tolist(),
        values=result.values.tolist()
    )


# ─── Pattern Detection ───────────────────────────────────────────

PATTERNS = {
    'rute_id': re.compile(r'\brute[_\s-]?(?:id\s*)?(\d{3})\b', re.IGNORECASE),
    'rute_code': re.compile(r'\b(ORG2ÅRH|ORG\d*\w+)\b', re.IGNORECASE),
    'postnr': re.compile(r'\b(\d{4})\b(?:\s+\w)'),
    'phone': re.compile(r'\b(\d{8})\b'),
    'error_code': re.compile(r'\berr(?:or)?[_\s-]?(?:code\s*)?(\d+)\b', re.IGNORECASE),
    'status': re.compile(r'\bstatus\s*(\d+)\b', re.IGNORECASE),
    'weekday': re.compile(r'\b(mandag|tirsdag|onsdag|torsdag|fredag|lørdag|søndag)\b', re.IGNORECASE),
    'month_name': re.compile(r'\b(januar|februar|marts|april|maj|juni|juli|august|september|oktober|november|december)\b', re.IGNORECASE),
}

MONTH_MAP = {
    'januar': 1, 'februar': 2, 'marts': 3, 'april': 4,
    'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
    'september': 9, 'oktober': 10, 'november': 11, 'december': 12
}


def detect_patterns(query):
    """Detect structured patterns in query, return filters"""
    detected = {}
    for name, pattern in PATTERNS.items():
        match = pattern.search(query)
        if match:
            detected[name] = match.group(1) if match.lastindex else match.group(0)
    return detected


def build_qdrant_filter(patterns, explicit_filters=None):
    """Build Qdrant filter from detected patterns and explicit filters"""
    conditions = []

    if explicit_filters:
        for key, value in explicit_filters.items():
            if key in ('rute_id_abs', 'year', 'month', 'disp_status', 'rute_status'):
                conditions.append(FieldCondition(key=key, match=MatchValue(value=int(value))))
            elif key in ('weekday', 'date', 'postnr', 'bynavn'):
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
            elif key in ('kunde', 'adresse', 'chf_rmrks'):
                conditions.append(FieldCondition(key=key, match=MatchText(text=value)))

    # Auto-detect from patterns
    if 'rute_id' in patterns and not any(c.key == 'rute_id_abs' for c in conditions):
        conditions.append(FieldCondition(key='rute_id_abs', match=MatchValue(value=int(patterns['rute_id']))))

    if 'weekday' in patterns and not any(c.key == 'weekday' for c in conditions):
        conditions.append(FieldCondition(key='weekday', match=MatchValue(value=patterns['weekday'].lower())))

    if 'month_name' in patterns and not any(c.key == 'month' for c in conditions):
        month_num = MONTH_MAP.get(patterns['month_name'].lower())
        if month_num:
            conditions.append(FieldCondition(key='month', match=MatchValue(value=month_num)))

    if not conditions:
        return None

    return Filter(must=conditions)


# ─── Temporal Decay ──────────────────────────────────────────────

import math
from datetime import datetime, date

# Collections where temporal decay applies (have date fields)
DECAY_COLLECTIONS = {"sessions", "conversations", "routes"}
# Evergreen collections — no decay
EVERGREEN_COLLECTIONS = {"advisor_brain", "miessler_bible", "knowledge"}

HALFLIFE_DAYS = 30  # Score halves every 30 days
DECAY_LAMBDA = math.log(2) / HALFLIFE_DAYS


def apply_temporal_decay(points, collection):
    """Apply exponential temporal decay to search results.

    Formula: adjusted_score = score × e^(-λ × age_days)
    where λ = ln(2) / halflife_days

    Evergreen collections (advisor_brain, miessler_bible) are not decayed.
    Points without a date field are not decayed.
    """
    if collection in EVERGREEN_COLLECTIONS:
        return points
    if collection not in DECAY_COLLECTIONS:
        return points

    today = date.today()
    for p in points:
        date_str = p.payload.get("date", "")
        if not date_str:
            continue
        try:
            point_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
            age_days = (today - point_date).days
            if age_days < 0:
                age_days = 0
            decay_factor = math.exp(-DECAY_LAMBDA * age_days)
            p.score = p.score * decay_factor
        except (ValueError, TypeError):
            pass

    # Re-sort by decayed score
    points.sort(key=lambda p: p.score, reverse=True)
    return points


# ─── Search Functions ─────────────────────────────────────────────

def collection_has_sparse(collection):
    """Tjek om collection har sparse vectors."""
    try:
        info = qdrant.get_collection(collection)
        sparse = info.config.params.sparse_vectors
        return sparse is not None and len(sparse) > 0
    except Exception:
        pass
    return False


def search_hybrid(query, collection="routes", limit=5, qdrant_filter=None):
    """Hybrid search: dense + sparse via RRF (Reciprocal Rank Fusion).
    Falder automatisk tilbage til dense-only hvis collection mangler sparse vectors."""
    if not collection_has_sparse(collection):
        return search_dense(query, collection, limit, qdrant_filter)

    dense_vector = get_dense_embedding(query)
    sparse_vector = get_sparse_embedding(query)

    results = qdrant.query_points(
        collection_name=collection,
        prefetch=[
            Prefetch(
                query=dense_vector,
                using="dense",
                limit=limit * 4,  # candidateMultiplier: 4
                filter=qdrant_filter,
            ),
            Prefetch(
                query=sparse_vector,
                using="sparse",
                limit=limit * 4,
                filter=qdrant_filter,
            ),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=limit * 2,  # Fetch extra for decay re-ranking
    )
    points = apply_temporal_decay(results.points, collection)
    return points[:limit]


def search_dense(query, collection="routes", limit=5, qdrant_filter=None):
    """Pure semantic search (dense vectors only)"""
    vector = get_dense_embedding(query)
    results = qdrant.query_points(
        collection_name=collection,
        query=vector,
        using="dense",
        limit=limit * 2,
        query_filter=qdrant_filter,
    )
    points = apply_temporal_decay(results.points, collection)
    return points[:limit]


def search_sparse(query, collection="routes", limit=5, qdrant_filter=None):
    """Pure keyword search (sparse/BM25 only)"""
    sparse_vector = get_sparse_embedding(query)
    results = qdrant.query_points(
        collection_name=collection,
        query=sparse_vector,
        using="sparse",
        limit=limit,
        query_filter=qdrant_filter,
    )
    return results.points


def search_filter_only(collection="routes", limit=10, qdrant_filter=None):
    """Metadata filter only (no vector search)"""
    if not qdrant_filter:
        return []
    results = qdrant.scroll(
        collection_name=collection,
        scroll_filter=qdrant_filter,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    return results[0]  # (points, next_offset)


def search_pattern(query, collection="routes", limit=10):
    """Pattern matching via payload text search"""
    # Try to find exact matches in text fields
    conditions = []

    # Search in kunde and adresse fields
    # Extract the most meaningful search term
    terms = re.sub(r'\b(find|søg|vis|alle|stops?|ruter?|i|på|med|for|fra|til)\b', '', query, flags=re.IGNORECASE).strip()
    if terms:
        # Search in multiple text fields
        results = []
        for field in ['kunde', 'adresse', 'chf_rmrks']:
            try:
                scroll_filter = Filter(must=[
                    FieldCondition(key=field, match=MatchText(text=terms))
                ])
                points, _ = qdrant.scroll(
                    collection_name=collection,
                    scroll_filter=scroll_filter,
                    limit=limit,
                    with_payload=True,
                    with_vectors=False,
                )
                results.extend(points)
            except:
                pass

        # Deduplicate by id
        seen = set()
        unique = []
        for p in results:
            if p.id not in seen:
                seen.add(p.id)
                unique.append(p)
        return unique[:limit]

    return []


def search_conversations_dense(query, limit=3):
    """Search conversations (hybrid with temporal decay)"""
    try:
        if collection_has_sparse("conversations"):
            return search_hybrid(query, "conversations", limit)
        vector = get_dense_embedding(query)
        results = qdrant.query_points(
            collection_name="conversations",
            query=vector,
            limit=limit * 2,
        )
        points = apply_temporal_decay(results.points, "conversations")
        return points[:limit]
    except Exception as e:
        print(f"Fejl ved søgning i conversations: {e}", file=sys.stderr)
        return []


def search_advisor(query, limit=5, author_filter=None, rerank=True):
    """Search advisor_brain collection (dense + cross-encoder reranking).
    Fetches top 20 via dense search, then reranks with cross-encoder to get top K."""
    qdrant_filter = None
    if author_filter:
        qdrant_filter = Filter(must=[
            FieldCondition(key="author", match=MatchValue(value=author_filter))
        ])
    try:
        vector = get_dense_embedding(query)
        fetch_limit = limit * 4 if rerank else limit
        results = qdrant.query_points(
            collection_name="advisor_brain",
            query=vector,
            using="dense",
            limit=fetch_limit,
            query_filter=qdrant_filter,
        )
        points = results.points

        if rerank and len(points) > 1:
            reranker = get_reranker()
            texts = [p.payload.get('text', p.payload.get('content', ''))[:500] for p in points]
            pairs = [(query, t) for t in texts]
            scores = reranker.predict(pairs)
            ranked = sorted(zip(points, scores), key=lambda x: x[1], reverse=True)
            points = [p for p, s in ranked[:limit]]

        return points[:limit]
    except Exception as e:
        print(f"Fejl ved søgning i advisor_brain: {e}", file=sys.stderr)
        return []


# ─── Retrieval Routing ────────────────────────────────────────────

def classify_query(query, patterns):
    """Determine best search strategy for a query"""
    has_patterns = bool(patterns)
    has_filter_patterns = any(k in patterns for k in ('rute_id', 'weekday', 'month_name'))

    # Pure filter query: "alle mandagsruter", "rute 231"
    if has_filter_patterns and len(query.split()) <= 5:
        return 'filter'

    # Pattern/exact query: codes, IDs, phone numbers
    if any(k in patterns for k in ('error_code', 'phone', 'rute_code')):
        return 'pattern'

    # Has some structured elements but also free text → hybrid + filter
    if has_filter_patterns:
        return 'hybrid_filtered'

    # Default: hybrid search
    return 'hybrid'


# ─── Formatting ───────────────────────────────────────────────────

def format_route_context(points):
    """Format route results"""
    if not points:
        return ""

    lines = ["## Relevante stops fra rutedata:\n"]
    for p in points:
        payload = p.payload
        score = getattr(p, 'score', None)
        score_str = f" (score: {score:.3f})" if score else ""

        lines.append(f"- **{payload.get('kunde', '?')}** ({payload.get('disp_headline', payload.get('headline', ''))}){score_str}")
        lines.append(f"  Adresse: {payload.get('adresse', '')} {payload.get('postnr', '')} {payload.get('bynavn', '')}")
        lines.append(f"  Rute: {payload.get('rute_headline', '')} | Dato: {payload.get('date', '?')} ({payload.get('weekday', '')})")

        if payload.get('lat') and payload.get('lng'):
            lines.append(f"  GPS: {payload.get('lat')}, {payload.get('lng')}")
        if payload.get('chf_rmrks'):
            lines.append(f"  Bemærk: {payload.get('chf_rmrks', '')[:100]}")
        lines.append("")

    return "\n".join(lines)


def format_conversation_context(points):
    """Format conversation results"""
    if not points:
        return ""

    lines = ["## Relevant fra tidligere samtaler:\n"]
    for p in points:
        payload = p.payload
        role = "Kris" if payload.get('role') == 'user' else "Claude"
        date = payload.get('date', '?')
        content = payload.get('content', '')[:300]
        lines.append(f"**[{date}] {role}:** {content}...")
        lines.append("")

    return "\n".join(lines)


def format_advisor_context(points):
    """Format advisor_brain results"""
    if not points:
        return ""

    author_labels = {"nate_jones": "Nate Jones", "miessler": "Miessler"}
    lines = ["## Advisor Brain:\n"]
    for p in points:
        payload = p.payload
        score = getattr(p, 'score', None)
        author = author_labels.get(payload.get('author', ''), payload.get('author', '?'))
        chapter = payload.get('chapter', '')
        section = payload.get('section', '')
        text = payload.get('text', '')[:400]
        score_str = f" [{score:.3f}]" if score else ""

        header = f"**[{author}]** {chapter}"
        if section:
            header += f" — {section}"
        header += score_str

        lines.append(header)
        lines.append(f"  {text}")
        lines.append("")

    return "\n".join(lines)


# ─── Main Entry Point ────────────────────────────────────────────

def get_context(query, search_routes=True, search_conversations=True,
                search_docs=True, search_advisor_brain=False,
                routes_limit=5, conv_limit=3,
                explicit_filters=None, force_mode=None,
                author_filter=None):
    """
    Main function: retrieve relevant context for a query.

    Args:
        query: Search text
        search_routes: Search route data
        search_conversations: Search conversations
        routes_limit: Max route results
        conv_limit: Max conversation results
        explicit_filters: Dict of field=value filters
        force_mode: Force search mode (hybrid/dense/sparse/filter/pattern)
    """
    context_parts = []
    search_info = []

    if search_routes:
        # Detect patterns
        patterns = detect_patterns(query)
        if patterns:
            search_info.append(f"Patterns: {patterns}")

        # Build filter
        qdrant_filter = build_qdrant_filter(patterns, explicit_filters)

        # Choose search strategy
        mode = force_mode or classify_query(query, patterns)
        search_info.append(f"Mode: {mode}")

        # Execute search
        if mode == 'filter':
            points = search_filter_only("routes", routes_limit, qdrant_filter)
        elif mode == 'pattern':
            points = search_pattern(query, "routes", routes_limit)
            # Also do filtered search if we have filters
            if qdrant_filter:
                filter_points = search_filter_only("routes", routes_limit, qdrant_filter)
                # Merge, dedup
                seen = set(p.id for p in points)
                for fp in filter_points:
                    if fp.id not in seen:
                        points.append(fp)
                        seen.add(fp.id)
                points = points[:routes_limit]
        elif mode == 'hybrid_filtered':
            points = search_hybrid(query, "routes", routes_limit, qdrant_filter)
        else:  # hybrid (default)
            points = search_hybrid(query, "routes", routes_limit, qdrant_filter)

        route_context = format_route_context(points)
        if route_context:
            context_parts.append(route_context)

    if search_conversations:
        conv_points = search_conversations_dense(query, conv_limit)
        conv_context = format_conversation_context(conv_points)
        if conv_context:
            context_parts.append(conv_context)

    if search_docs:
        try:
            doc_points = search_dense(query, "docs", min(routes_limit, 3))
            if doc_points:
                doc_lines = ["\n### Docs (etableret viden)\n"]
                for p in doc_points:
                    score = getattr(p, 'score', 0)
                    file = p.payload.get('file', '?')
                    header = p.payload.get('header', '')
                    content = p.payload.get('summary', '')[:200]
                    doc_lines.append(f"**{file}** ({header}) [{score:.2f}]")
                    doc_lines.append(f"  {content}\n")
                context_parts.append("\n".join(doc_lines))
        except Exception:
            pass  # docs collection may not exist

    if search_advisor_brain:
        advisor_points = search_advisor(query, routes_limit, author_filter)
        advisor_context = format_advisor_context(advisor_points)
        if advisor_context:
            context_parts.append(advisor_context)

    if search_info:
        header = f"_Søgning: {' | '.join(search_info)}_\n"
        context_parts.insert(0, header)

    if not context_parts:
        return "Ingen relevant kontekst fundet."

    return "\n---\n\n".join(context_parts)


def parse_filters(filter_str):
    """Parse 'key=value,key2=value2' into dict"""
    if not filter_str:
        return None
    filters = {}
    for pair in filter_str.split(','):
        if '=' in pair:
            key, value = pair.split('=', 1)
            filters[key.strip()] = value.strip()
    return filters


def main():
    parser = argparse.ArgumentParser(description='Hent kontekst fra Qdrant (v2 hybrid)')
    parser.add_argument('query', help='Søgetekst')
    parser.add_argument('--routes', '-r', action='store_true', help='Kun søg i ruter')
    parser.add_argument('--conversations', '-c', action='store_true', help='Kun søg i samtaler')
    parser.add_argument('--docs', '-d', action='store_true', help='Kun søg i docs (etableret viden)')
    parser.add_argument('--limit', '-l', type=int, default=5, help='Max resultater per collection')
    parser.add_argument('--filter', '-f', type=str, help='Metadata filter: key=value,key2=value2')
    parser.add_argument('--mode', '-m', choices=['hybrid', 'dense', 'sparse', 'filter', 'pattern'],
                        help='Force search mode')
    parser.add_argument('--exact', '-e', action='store_true', help='Pattern/exact match mode')
    parser.add_argument('--advisor', '-a', action='store_true', help='Søg i advisor_brain (Nate Jones + Miessler)')
    parser.add_argument('--author', type=str, choices=['nate', 'miessler'], help='Filtrér advisor på forfatter')
    parser.add_argument('--json', '-j', action='store_true', help='Output som JSON')

    args = parser.parse_args()

    any_specified = args.routes or args.conversations or args.docs or args.advisor
    search_routes = args.routes or not any_specified
    search_conversations = args.conversations or not any_specified
    search_docs = args.docs or not any_specified
    search_advisor_brain = args.advisor

    # Map author shorthand
    author_filter = None
    if args.author:
        author_filter = "nate_jones" if args.author == "nate" else "miessler"

    explicit_filters = parse_filters(args.filter)
    force_mode = args.mode or ('pattern' if args.exact else None)

    if args.json:
        # JSON output
        patterns = detect_patterns(args.query)
        qdrant_filter = build_qdrant_filter(patterns, explicit_filters)
        mode = force_mode or classify_query(args.query, patterns)

        result = {
            "query": args.query,
            "mode": mode,
            "patterns": patterns,
            "routes": [],
            "conversations": []
        }

        if search_routes:
            if mode == 'filter':
                points = search_filter_only("routes", args.limit, qdrant_filter)
            elif mode == 'pattern':
                points = search_pattern(args.query, "routes", args.limit)
            elif mode == 'hybrid_filtered':
                points = search_hybrid(args.query, "routes", args.limit, qdrant_filter)
            else:
                points = search_hybrid(args.query, "routes", args.limit, qdrant_filter)

            for p in points:
                result["routes"].append({
                    "score": getattr(p, 'score', None),
                    "payload": p.payload
                })

        if search_conversations:
            for p in search_conversations_dense(args.query, min(args.limit, 3)):
                result["conversations"].append({
                    "score": p.score,
                    "payload": p.payload
                })

        if search_advisor_brain:
            result["advisor"] = []
            for p in search_advisor(args.query, args.limit, author_filter):
                result["advisor"].append({
                    "score": getattr(p, 'score', None),
                    "payload": p.payload
                })

        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        context = get_context(
            args.query,
            search_routes=search_routes,
            search_conversations=search_conversations,
            search_docs=search_docs,
            search_advisor_brain=search_advisor_brain,
            routes_limit=args.limit,
            conv_limit=min(args.limit, 3),
            explicit_filters=explicit_filters,
            force_mode=force_mode,
            author_filter=author_filter,
        )
        print(context)


if __name__ == "__main__":
    main()
