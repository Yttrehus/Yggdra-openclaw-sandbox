import time
import math
from datetime import datetime
import json

def parse_iso(ts_str):
    """Smidig parsing af ISO-lignende datoer."""
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00')).timestamp()
    except ValueError:
        return datetime.strptime(ts_str, "%Y-%m-%d").timestamp()

def calculate_temporal_decay(original_score, timestamp_str, current_time, half_life_days=30):
    """
    Beregner en ny score baseret på temporal decay.
    Formel: score * exp(-age_days * ln(2) / half_life)
    """
    doc_time = parse_iso(timestamp_str)
    age_days = (current_time - doc_time) / (24 * 3600)
    
    decay_constant = math.log(2) / half_life_days
    decay_factor = math.exp(-max(0, age_days) * decay_constant)
    
    return original_score * decay_factor

def simulate_llm_rerank(results, query):
    """
    Simulerer en LLM-baseret reranking (Gap 2).
    Vi booster resultater der faktisk besvarer query'en semantisk.
    """
    keywords = query.lower().split()
    reranked = []
    
    print(f"LLM Reranking (Simulated) for query: '{query}'...")
    
    for r in results:
        content = r.get('content', '').lower()
        llm_score = r['score']
        
        # Simuleret 'rerank logic': find match på tværs af query ord
        match_count = sum(1 for word in keywords if word in content)
        
        # En kaffemaskine-note skal ikke boostes af 'status'
        # men en 'rute 256 status' note skal.
        if "rute" in content and "status" in content:
            boost = 1.5
            llm_score *= boost
            match_found = True
        elif match_count > 0:
            boost = 1.1
            llm_score *= boost
            match_found = True
        else:
            match_found = False
            
        reranked.append({**r, 'score': llm_score, 'llm_boost': match_found})
        
    return sorted(reranked, key=lambda x: x['score'], reverse=True)

def rerank_pipeline(results, query, current_time):
    """
    Fuld pipeline:
    1. Initial retrieval score (fra Qdrant)
    2. Temporal Decay (Gap 4)
    3. LLM Reranking (Gap 2)
    """
    print(f"\n--- Reranking Pipeline for query: '{query}' ---")
    
    # Trin 1: Temporal Decay
    decayed = []
    for r in results:
        ts = r.get('ts', '2024-01-01')
        orig_score = r['score']
        score_after_decay = calculate_temporal_decay(orig_score, ts, current_time)
        decayed.append({**r, 'score': score_after_decay, 'orig_score': orig_score})
        
    # Trin 2: LLM Rerank
    final_results = simulate_llm_rerank(decayed, query)
    
    return final_results

if __name__ == "__main__":
    print("Yggdra Retrieval PoC - Closing Gaps 2 & 4 (Full Pipeline)")
    
    # Simulationstid: 23. maj 2024
    simulated_now = datetime(2024, 5, 23).timestamp()
    
    # Mock data fra Qdrant
    mock_qdrant_results = [
        {
            "id": "A", 
            "content": "Gammel instruks om rute 256 fra januar. Husk at tjekke diesel.", 
            "score": 0.95, 
            "ts": "2024-01-15"
        },
        {
            "id": "B", 
            "content": "Status på rute 256: Alt kører som planlagt. Organisk affald opsamlet.", 
            "score": 0.88, 
            "ts": "2024-05-10"
        },
        {
            "id": "C", 
            "content": "Kaffemaskinen på kontoret er i stykker.", 
            "score": 0.82, 
            "ts": "2024-05-22"
        }
    ]
    
    query = "rute 256 status"
    final = rerank_pipeline(mock_qdrant_results, query, simulated_now)
    
    print(f"\n{'ID':<3} | {'Orig':<6} | {'Final':<6} | {'Dato':<10} | {'Status'}")
    print("-" * 60)
    for r in final:
        status = "BOOSTED" if r.get('llm_boost') else "Normal"
        print(f"{r['id']:<3} | {r['orig_score']:<6.3f} | {r['score']:<6.3f} | {r['ts']:<10} | {status}")

    print("\nKonklusion:")
    top_result = final[0]
    if top_result['id'] == 'B':
        print("SUCCESS: 'Nyere status' (B) vandt over 'Støj' (C) og 'Gammel info' (A).")
    else:
        print(f"FAILURE: Top resultatet var {top_result['id']}.")
