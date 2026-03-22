import json
import os

class Reranker:
    """
    Simuleret reranker til Gap 2.
    I produktion vil denne bruge Cohere Rerank API eller en lokal Cross-Encoder.
    """
    def __init__(self, model="cohere-rerank-v3"):
        self.model = model

    def rerank(self, query, results, top_n=5):
        """
        Sorterer resultater baseret på semantisk relevans (simuleret).
        I en rigtig implementering sendes (query, [doc1, doc2...]) til API'et.
        """
        if not results:
            return []

        # Her simulerer vi LLM-baseret reranking ved at kigge efter keyword-match
        # som Qdrant's dense search måske har overset, men som en reranker ville fange.
        scored_results = []
        for r in results:
            text = r['payload'].get('text', '').lower()
            original_score = r['score']
            
            # Simuleret boost hvis query keywords findes i teksten
            boost = 0.0
            query_words = query.lower().replace('?', '').split()
            for word in query_words:
                if len(word) > 4 and word in text:
                    boost += 0.1
            
            r['rerank_score'] = min(1.0, r['score'] + boost)
            scored_results.append(r)

        return sorted(scored_results, key=lambda x: x['rerank_score'], reverse=True)[:top_n]

if __name__ == "__main__":
    print("Reranker module initialized.")
