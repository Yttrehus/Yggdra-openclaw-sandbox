import time
import math
from datetime import datetime

def parse_iso(ts_str):
    """Smidig parsing af ISO-lignende datoer."""
    try:
        return datetime.fromisoformat(ts_str).timestamp()
    except ValueError:
        return datetime.strptime(ts_str, "%Y-%m-%d").timestamp()

def calculate_temporal_decay(original_score, timestamp_str, current_time, half_life_days=30):
    """
    Beregner en ny score baseret på temporal decay.
    Gap 4 fra ai-frontier/GAPS.md
    Formel: score * exp(-age_days * ln(2) / half_life)
    """
    doc_time = parse_iso(timestamp_str)
    
    age_days = (current_time - doc_time) / (24 * 3600)
    
    # ln(2) / half_life giver den præcise halveringstid
    decay_constant = math.log(2) / half_life_days
    decay_factor = math.exp(-max(0, age_days) * decay_constant)
    
    return original_score * decay_factor

def rerank_results(results, query, current_time):
    """
    Simulerer en reranking af resultater.
    Gap 2 fra ai-frontier/GAPS.md
    Kombinerer original semantisk score med temporal decay.
    """
    print(f"\n--- Reranking {len(results)} results for query: '{query}' ---")
    
    reranked = []
    for r in results:
        decayed_score = calculate_temporal_decay(r['score'], r['ts'], current_time)
        reranked.append({
            **r,
            'original_score': r['score'],
            'score': decayed_score,
            'decay_pct': (1 - (decayed_score / r['score'])) * 100
        })
    
    # Sortér efter den nye vægtede score
    return sorted(reranked, key=lambda x: x['score'], reverse=True)

if __name__ == "__main__":
    print("Yggdra Retrieval PoC - Closing Gaps 2 & 4")
    
    # Vi bruger den aktuelle simulationstid (Session 24 context er Maj 2024)
    # Men vi har brug for en reference der passer til data.
    # Da mock-data er Maj 2024, sætter vi "nu" til 23. maj 2024.
    simulated_now = datetime(2024, 5, 23).timestamp()
    
    # Simulation med realistiske datoer
    mock_results = [
        {"id": "Gammel men relevant", "score": 0.95, "ts": "2024-01-15"},
        {"id": "Nyere", "score": 0.88, "ts": "2024-05-10"},
        {"id": "Helt ny", "score": 0.82, "ts": "2024-05-22"}
    ]
    
    results = rerank_results(mock_results, "rute 256 status", simulated_now)
    
    print(f"{'ID':<25} | {'Orig':<6} | {'Decayed':<7} | {'Tab %':<6}")
    print("-" * 55)
    for r in results:
        print(f"{r['id']:<25} | {r['original_score']:<6.3f} | {r['score']:<7.3f} | {r['decay_pct']:>5.1f}%")
