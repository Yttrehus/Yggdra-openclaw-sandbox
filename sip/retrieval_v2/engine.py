import math
from datetime import datetime

class ContextReranker:
    """
    Reranking logik til forbedring af retrieval kvalitet.
    Implementerer Gap 2 (Reranking) og Gap 4 (Temporal Decay).
    """
    
    def __init__(self, half_life_days=30):
        self.half_life_days = half_life_days
        self.decay_constant = math.log(2) / half_life_days

    def _parse_ts(self, ts_str):
        try:
            return datetime.fromisoformat(ts_str.replace('Z', '+00:00')).timestamp()
        except ValueError:
            return datetime.strptime(ts_str, "%Y-%m-%d").timestamp()

    def apply_decay(self, score, ts_str, current_ts):
        doc_ts = self._parse_ts(ts_str)
        age_days = (current_ts - doc_ts) / (24 * 3600)
        decay_factor = math.exp(-max(0, age_days) * self.decay_constant)
        return score * decay_factor

    def rerank(self, results, query, current_ts=None):
        if current_ts is None:
            current_ts = datetime.now().timestamp()
            
        keywords = query.lower().split()
        reranked = []
        
        for r in results:
            # 1. Start med original score
            score = r.get('score', 0.5)
            
            # 2. Påfør temporal decay
            if 'ts' in r:
                score = self.apply_decay(score, r['ts'], current_ts)
            
            # 3. Simuleret LLM/Heuristisk Rerank boost
            content = r.get('content', '').lower()
            boost = 1.0
            
            # Matcher query'en præcist (simple heuristikker)
            if all(k in content for k in keywords):
                boost = 1.5
            elif any(k in content for k in keywords):
                boost = 1.2
                
            final_score = score * boost
            reranked.append({
                **r,
                'final_score': final_score,
                'boosted': boost > 1.0
            })
            
        return sorted(reranked, key=lambda x: x['final_score'], reverse=True)

if __name__ == "__main__":
    # Test simulation
    engine = ContextReranker()
    now = datetime(2024, 5, 23).timestamp()
    
    mock_data = [
        {"id": "OldInfo", "content": "Rute 256 instruks fra januar.", "score": 0.9, "ts": "2024-01-01"},
        {"id": "NewStatus", "content": "Rute 256 status er grøn.", "score": 0.8, "ts": "2024-05-20"},
        {"id": "Noise", "content": "Vejret er godt i dag.", "score": 0.7, "ts": "2024-05-22"}
    ]
    
    ranked = engine.rerank(mock_data, "rute 256 status", current_ts=now)
    
    print(f"{'ID':<15} | {'Score':<10}")
    print("-" * 30)
    for r in ranked:
        print(f"{r['id']:<15} | {r['final_score']:.4f}")
