import os
import sys
import json

# Setup paths
sys.path.append(os.path.abspath('scripts'))
from get_context import search_hybrid, is_evergreen

def test_v2_final():
    print("--- Testing Context Retrieval v2.1 Final Integration ---")
    
    # Simuleret query der burde trigge keyword boost
    query = "vision for Yggdra exoskeleton"
    
    # I denne sandkasse kan vi ikke kalde det rigtige Qdrant uden tunnel
    # Men vi kan teste post-processing logikken i isolation
    
    class MockPoint:
        def __init__(self, id, score, payload):
            self.id = id
            self.score = score
            self.payload = payload
            self.decay_factor = 1.0
            self.rerank_score = 0.0

    points = [
        MockPoint('1', 0.4, {'text': 'Yggdra vision: et kognitivt exoskeleton', 'source': 'BLUEPRINT.md'}),
        MockPoint('2', 0.8, {'text': 'Vi har købt mælk', 'source': 'notes.md', 'date': '2026-03-23'}),
        MockPoint('3', 0.6, {'text': 'Exoskeleton patterns', 'source': 'research.md', 'date': '2026-01-01'})
    ]

    from get_context import rerank_results, apply_decay
    
    print(f"Query: {query}")
    print("\nStep 1: Raw results")
    for p in points:
        print(f"  {p.id}: {p.score} | {p.payload['text']}")

    print("\nStep 2: Applying Decay & Evergreen Protection")
    points = apply_decay(points, 'sessions')
    for p in points:
        ev = " [EVERGREEN]" if is_evergreen(p.payload) else ""
        print(f"  {p.id}: {p.score:.3f}{ev}")

    print("\nStep 3: Reranking with Keyword Boost (+0.40)")
    final = rerank_results(query, points, limit=3)
    for p in final:
        print(f"  {p.id}: {p.rerank_score:.3f} | {p.payload['text']}")

if __name__ == "__main__":
    test_v2_final()
