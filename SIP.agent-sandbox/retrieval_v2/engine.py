import math
import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional

class ContextReranker:
    """
    Reranking logik til forbedring af retrieval kvalitet.
    Implementerer Fase 1 af Memory Architecture (Gap 2 & 4).
    """
    
    def __init__(self, half_life_days: float = 30.0):
        self.half_life_days = half_life_days
        # lambda = ln(2) / half_life
        self.decay_constant = math.log(2) / self.half_life_days

    def _parse_ts(self, ts_str: str) -> datetime:
        """Smidig parsing af ISO timestamps."""
        try:
            # Håndter Z-suffix og offset
            clean_ts = ts_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(clean_ts)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            # Fallback til YYYY-MM-DD
            return datetime.strptime(ts_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    def apply_decay(self, score: float, created_at: str, current_ts: Optional[datetime] = None) -> (float, float):
        """Beregner decayed score og returnerer (new_score, decay_factor)."""
        if current_ts is None:
            current_ts = datetime.now(timezone.utc)
            
        doc_ts = self._parse_ts(created_at)
        age_days = (current_ts - doc_ts).total_seconds() / (24 * 3600)
        
        # Decay factor: e^(-lambda * t)
        decay_factor = math.exp(-max(0, age_days) * self.decay_constant)
        return score * decay_factor, decay_factor

    def rerank(self, results: List[Dict], query: str, current_ts: Optional[datetime] = None) -> List[Dict]:
        """
        Kombinerer temporal decay med semantisk relevans-boost.
        """
        if current_ts is None:
            current_ts = datetime.now(timezone.utc)
            
        keywords = query.lower().split()
        reranked = []
        
        for r in results:
            # 1. Start med original semantisk score (dense/hybrid)
            original_score = r.get('score', 0.5)
            
            # 2. Påfør temporal decay hvis dato findes
            created_at = r.get('payload', {}).get('created_at') or r.get('created_at')
            decay_factor = 1.0
            score = original_score
            
            if created_at:
                score, decay_factor = self.apply_decay(original_score, created_at, current_ts)
            
            # 3. Semantisk Rerank boost (simuleret cross-encoder/LLM logik)
            # Vi booster resultater der har keyword overlap i vigtige felter
            text_to_scan = ""
            payload = r.get('payload', {})
            text_to_scan += payload.get('title', '') + " "
            text_to_scan += payload.get('heading', '') + " "
            text_to_scan += payload.get('text', '') or r.get('text', '')
            text_to_scan = text_to_scan.lower()
            
            relevance_boost = 1.0
            if all(k in text_to_scan for k in keywords):
                relevance_boost = 1.5 # Præcist match på alle ord
            elif any(k in text_to_scan for k in keywords):
                relevance_boost = 1.2 # Delvist match
                
            final_score = score * relevance_boost
            
            new_result = dict(r)
            new_result['final_score'] = final_score
            new_result['decay_factor'] = decay_factor
            new_result['relevance_boost'] = relevance_boost
            reranked.append(new_result)
            
        # Sorter efter den nye kombinerede score
        return sorted(reranked, key=lambda x: x['final_score'], reverse=True)

if __name__ == "__main__":
    # Demo/Test
    engine = ContextReranker(half_life_days=30)
    now = datetime.now(timezone.utc)
    
    mock_results = [
        {
            "id": "OldRelevant", 
            "score": 0.9, 
            "created_at": "2026-01-15T12:00:00Z",
            "text": "Rute 256 instruks: Gamle retningslinjer for organisk affald."
        },
        {
            "id": "NewStatus", 
            "score": 0.75, 
            "created_at": now.isoformat(),
            "text": "Status opdatering: Rute 256 kører normalt i dag."
        },
        {
            "id": "Noise", 
            "score": 0.85, 
            "created_at": now.isoformat(),
            "text": "Vejret i Aarhus er overskyet."
        }
    ]
    
    query = "rute 256 status"
    results = engine.rerank(mock_results, query, now)
    
    print(f"Query: '{query}'\n")
    print(f"{'ID':<15} | {'Orig':<6} | {'Final':<6} | {'Decay':<6} | {'Boost'}")
    print("-" * 55)
    for r in results:
        print(f"{r['id']:<15} | {r['score']:<6.3f} | {r['final_score']:<6.3f} | {r['decay_factor']:<6.3f} | {r['relevance_boost']:.1f}x")
