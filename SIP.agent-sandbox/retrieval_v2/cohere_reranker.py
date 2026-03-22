import os
import requests
import json

class CohereReranker:
    """
    Rigtig reranker implementation ved hjælp af Cohere Rerank API.
    Kræver COHERE_API_KEY miljøvariabel.
    """
    def __init__(self, api_key=None, model="rerank-v3.0"):
        self.api_key = api_key or os.environ.get("COHERE_API_KEY")
        self.model = model
        self.url = "https://api.cohere.ai/v1/rerank"

    def rerank(self, query, results, top_n=5):
        if not self.api_key:
            print("Warning: COHERE_API_KEY not found. Falling back to mock reranker.")
            from .reranker import Reranker
            return Reranker().rerank(query, results, top_n)

        if not results:
            return []

        # Forbered dokumenter til Cohere (maks 1000 per kald)
        documents = [r['payload'].get('text', str(r['payload'])) for r in results[:100]]
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "query": query,
            "documents": documents,
            "top_n": top_n,
            "return_documents": False
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            rerank_results = response.json().get('results', [])
            
            final_results = []
            for res in rerank_results:
                idx = res['index']
                point = results[idx]
                point['rerank_score'] = res['relevance_score']
                final_results.append(point)
                
            return final_results
        except Exception as e:
            print(f"Error during Cohere rerank: {e}. Falling back to mock.")
            from .reranker import Reranker
            return Reranker().rerank(query, results, top_n)

if __name__ == "__main__":
    print("Cohere Reranker module initialized.")
