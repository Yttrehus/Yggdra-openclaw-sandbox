import math
import json
import os
from datetime import datetime, timezone

class TemporalReranker:
    """
    Implementering af Fase 1 i Memory Architecture:
    Temporal Decay: score *= exp(-age_days / half_life)
    
    Standard half_life er 30 dage.
    """
    def __init__(self, half_life_days=30):
        self.half_life_days = half_life_days
        # decay_constant lambda = ln(2) / half_life
        self.decay_constant = math.log(2) / self.half_life_days

    def calculate_decay(self, original_score, created_at_iso):
        """Beregner decayed score baseret på ISO timestamp."""
        try:
            # Håndter både Z og +00:00
            ts_str = created_at_iso.replace('Z', '+00:00')
            created_dt = datetime.fromisoformat(ts_str)
            
            # Sørg for at begge er offset-aware (UTC)
            now = datetime.now(timezone.utc)
            if created_dt.tzinfo is None:
                created_dt = created_dt.replace(tzinfo=timezone.utc)
                
            age_days = (now - created_dt).total_seconds() / (24 * 3600)
            
            # Decay formel: e^(-lambda * t)
            decay_factor = math.exp(-max(0, age_days) * self.decay_constant)
            
            return original_score * decay_factor, decay_factor
        except Exception as e:
            return original_score, 1.0

    def rerank(self, points):
        scored_points = []
        for p in points:
            original_score = p.get('score', 0.0)
            created_at = p.get('payload', {}).get('created_at', datetime.now(timezone.utc).isoformat())
            
            new_score, factor = self.calculate_decay(original_score, created_at)
            
            new_point = dict(p)
            new_point['decayed_score'] = new_score
            new_point['decay_factor'] = factor
            scored_points.append(new_point)
            
        return sorted(scored_points, key=lambda x: x['decayed_score'], reverse=True)

if __name__ == "__main__":
    reranker = TemporalReranker(half_life_days=30)
    
    test_points = [
        {
            "id": "ny-og-relevant",
            "score": 0.8,
            "payload": {"created_at": datetime.now(timezone.utc).isoformat(), "text": "Helt ny viden"}
        },
        {
            "id": "gammel-men-stærk",
            "score": 0.95,
            "payload": {"created_at": "2026-01-01T12:00:00Z", "text": "Meget gammel viden"}
        }
    ]
    
    print("--- Temporal Reranking Test ---")
    results = reranker.rerank(test_points)
    for r in results:
        print(f"ID: {r['id']}")
        print(f"  Original Score: {r['score']:.4f}")
        print(f"  Decayed Score:  {r['decayed_score']:.4f}")
        print(f"  Factor:         {r['decay_factor']:.4f}")
