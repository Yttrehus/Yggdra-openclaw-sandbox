import sys
import os
from datetime import datetime, timezone, timedelta
import json

# Tilføj SIP mappen til path for at importere engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from retrieval_v2.engine import RetrievalEngineV2

def run_synthetic_test():
    engine = RetrievalEngineV2(half_life_days=30)
    now = datetime.now(timezone.utc)
    
    print("--- Yggdra Synthetic Retrieval Benchmark ---")
    print(f"Simulationstid: {now.isoformat()}\n")

    # Scenarier
    mock_data = [
        {
            "id": "NEW-WEAK",
            "score": 0.80,
            "payload": {
                "text": "Status opdatering: Vi er i gang med Session 34.",
                "created_at": (now - timedelta(minutes=5)).isoformat(),
                "source": "memory/2026-03-22.md"
            }
        },
        {
            "id": "OLD-STRONG",
            "score": 0.95,
            "payload": {
                "text": "Beslutning fra januar: Vi bruger Docker til alle services.",
                "created_at": (now - timedelta(days=60)).isoformat(),
                "source": "memory/2026-01-20.md"
            }
        },
        {
            "id": "EVERGREEN-OLD",
            "score": 0.85,
            "payload": {
                "text": "System Vision: Yggdra er et kognitivt exoskeleton.",
                "created_at": (now - timedelta(days=365)).isoformat(),
                "source": "BLUEPRINT.md"
            }
        }
    ]

    # Test med query for reranker boost
    query = "Hvad er visionen for exoskeleton?"
    processed = engine.process_results(mock_data, query=query)

    print(f"\n--- Resultater efter Temporal Decay & Reranking (Query: '{query}') ---")
    print(f"{'ID':<15} | {'Orig':<6} | {'Decay':<6} | {'Rerank':<6} | {'Status'}")
    print("-" * 70)
    
    for r in processed:
        status = "EVERGREEN" if r['is_evergreen'] else "DECAYED"
        print(f"{r['id']:<15} | {r['original_score']:<6.3f} | {r['score']:<6.3f} | {r['rerank_score']:<6.3f} | {status}")

    print("\nKonklusion:")
    if processed[0]['id'] == 'EVERGREEN-OLD':
        print("SUCCESS: Evergreen protection virker (1 år gammel vision topper listen).")
    
    if processed[1]['id'] == 'NEW-WEAK':
        print("SUCCESS: Temporal decay virker (5 min gammel note slår 60 dage gammel beslutning).")

if __name__ == "__main__":
    run_synthetic_test()
