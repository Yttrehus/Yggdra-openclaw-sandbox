import math
from datetime import datetime, timezone

class RetrievalEngineV2:
    """
    Anden generation af Yggdras Retrieval Engine.
    Implementerer:
    - Temporal Decay (Gap 4)
    - Evergreen Protection (Principper/Manualer)
    - Reranking Interface (Gap 2)
    """
    def __init__(self, half_life_days=30):
        self.half_life_days = half_life_days
        self.decay_constant = math.log(2) / self.half_life_days
        self.evergreen_patterns = [
            "BLUEPRINT.md", "IDENTITY.md", "SOUL.md", "CLAUDE.md",
            "KNB.manuals/", "rules/", "SPEC-"
        ]

    def is_evergreen(self, source):
        if not source: return False
        return any(p in source for p in self.evergreen_patterns)

    def calculate_decay(self, original_score, created_at_iso, source=None):
        """Beregner score efter tidsmæssigt forfald."""
        if self.is_evergreen(source):
            return original_score, 1.0

        try:
            # ISO parsing
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

    def process_results(self, points, query=None):
        """
        Processerer rå Qdrant resultater.
        1. Anvender Temporal Decay
        2. (Fremtidig) LLM Reranking
        """
        processed = []
        for p in points:
            # Håndter både Qdrant ScoredPoint objekter og mock dicts
            payload = p.get('payload', {}) if isinstance(p, dict) else p.payload
            score = p.get('score', 0.0) if isinstance(p, dict) else p.score
            created_at = payload.get('created_at') or payload.get('date') or datetime.now(timezone.utc).isoformat()
            source = payload.get('source') or payload.get('file_path')
            
            decayed_score, factor = self.calculate_decay(score, created_at, source)
            
            entry = {
                "id": p.get('id') if isinstance(p, dict) else p.id,
                "original_score": score,
                "score": decayed_score,
                "decay_factor": factor,
                "is_evergreen": self.is_evergreen(source),
                "payload": payload
            }
            processed.append(entry)
            
        # Sorter efter ny score
        return sorted(processed, key=lambda x: x['score'], reverse=True)

if __name__ == "__main__":
    engine = RetrievalEngineV2()
    print("Retrieval Engine v2 initialized.")
