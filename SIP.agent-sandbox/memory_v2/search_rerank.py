import math
import sys
import json
from datetime import datetime, timezone
import os

# Tilføj roden til path så vi kan importere reranker hvis nødvendigt, 
# men her holder vi det selvstændigt for PoC.

class TemporalReranker:
    def __init__(self, half_life_days=30):
        self.half_life_days = half_life_days
        self.decay_constant = math.log(2) / self.half_life_days

    def calculate_decay(self, original_score, created_at_iso):
        try:
            ts_str = created_at_iso.replace('Z', '+00:00')
            created_dt = datetime.fromisoformat(ts_str)
            now = datetime.now(timezone.utc)
            if created_dt.tzinfo is None:
                created_dt = created_dt.replace(tzinfo=timezone.utc)
            age_days = (now - created_dt).total_seconds() / (24 * 3600)
            decay_factor = math.exp(-max(0, age_days) * self.decay_constant)
            return original_score * decay_factor, decay_factor
        except Exception:
            return original_score, 1.0

    def rerank(self, points):
        scored_points = []
        for p in points:
            original_score = p.get('score', 0.0)
            created_at = p.get('payload', {}).get('created_at') or p.get('created_at') or datetime.now(timezone.utc).isoformat()
            new_score, factor = self.calculate_decay(original_score, created_at)
            new_point = dict(p)
            new_point['decayed_score'] = new_score
            new_point['decay_factor'] = factor
            scored_points.append(new_point)
        return sorted(scored_points, key=lambda x: x['decayed_score'], reverse=True)

def mock_search_and_rerank(query):
    print(f"Søger efter: '{query}' (Simuleret hybrid search + rerank)\n")
    
    # 1. Simuleret rå search output fra Qdrant
    mock_raw_results = [
        {
            "id": 1,
            "score": 0.95,
            "created_at": "2026-01-10T10:00:00Z",
            "text": "Beslutning: Vi bruger Qdrant som primær vektor-database for Yggdra.",
            "title": "Hukommelsesarkitektur v1"
        },
        {
            "id": 2,
            "score": 0.88,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "text": "Implementering af temporal decay reranking i SIP sandbox.",
            "title": "Agent Session 32"
        },
        {
            "id": 3,
            "score": 0.70,
            "created_at": "2025-12-01T09:00:00Z",
            "text": "Gammel research om Pinecone og Weaviate.",
            "title": "Vektor DB Evaluering 2025"
        }
    ]
    
    # 2. Anvend Temporal Reranking
    reranker = TemporalReranker(half_life_days=30)
    reranked = reranker.rerank(mock_raw_results)
    
    # 3. Print resultater
    print(f"{'Rank':<5} | {'Titel':<25} | {'Orig':<6} | {'Decayed':<7} | {'Alder'}")
    print("-" * 70)
    for i, r in enumerate(reranked, 1):
        ts = datetime.fromisoformat(r['created_at'].replace('Z', '+00:00'))
        days_ago = (datetime.now(timezone.utc) - ts).days
        print(f"{i:<5} | {r['title'][:25]:<25} | {r['score']:<6.3f} | {r['decayed_score']:<7.3f} | {days_ago} dage")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "hukommelse"
    mock_search_and_rerank(query)
