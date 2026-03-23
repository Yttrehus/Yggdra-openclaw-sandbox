import os
import sys

# Simuler mock points
class MockPoint:
    def __init__(self, id, score, payload):
        self.id = id
        self.score = score
        self.payload = payload

def test_rerank():
    # Tilføj scripts til path
    sys.path.append(os.path.abspath('scripts'))
    from get_context import rerank_results
    
    query = "Hvad er visionen for Yggdra?"
    
    points = [
        MockPoint('1', 0.5, {'text': 'Yggdra er et personligt kognitivt exoskeleton.'}),
        MockPoint('2', 0.8, {'text': 'Vi spiste pizza i går.'}),
        MockPoint('3', 0.4, {'text': 'Her er en note om vision og exoskeleton.'})
    ]
    
    print(f"Original rækkefølge (score):")
    for p in sorted(points, key=lambda x: x.score, reverse=True):
        print(f"  {p.id}: {p.score} - {p.payload['text']}")
        
    reranked = rerank_results(query, points, limit=3)
    
    print(f"\nReranked rækkefølge (keyword fallback boost):")
    for p in reranked:
        print(f"  {p.id}: {p.rerank_score:.3f} - {p.payload['text']}")

if __name__ == "__main__":
    test_rerank()
