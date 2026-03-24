import os
import sys
import json
from datetime import datetime, timezone

# Tilføj roden til path
sys.path.append(os.path.abspath('scripts'))
from get_context import is_evergreen, apply_decay

def test_live_logic():
    # 1. Test Evergreen Detection
    test_payloads = [
        {'source': 'BLUEPRINT.md', 'text': 'Vision info'},
        {'file_path': 'manuals/git.md', 'text': 'Git guide'},
        {'is_evergreen': True, 'fact': 'Vigtig beslutning'},
        {'source': 'random_note.md', 'text': 'Uvigtig info'}
    ]
    
    print("--- Evergreen Detection Test ---")
    for p in test_payloads:
        print(f"Source: {p.get('source', p.get('file_path', 'N/A')):<20} | Evergreen: {is_evergreen(p)}")

    # 2. Test Decay Application
    class MockPoint:
        def __init__(self, id, score, payload):
            self.id = id
            self.score = score
            self.payload = payload
            self.decay_factor = 1.0

    points = [
        MockPoint('OLD', 1.0, {'date': '2026-01-01T00:00:00Z', 'source': 'old.md'}),
        MockPoint('NEW', 1.0, {'date': datetime.now(timezone.utc).isoformat(), 'source': 'new.md'}),
        MockPoint('EVER', 1.0, {'is_evergreen': True, 'date': '2026-01-01T00:00:00Z'})
    ]
    
    print("\n--- Decay Application Test (Halflife 30 days) ---")
    decayed = apply_decay(points, 'sessions')
    for p in decayed:
        print(f"ID: {p.id:<5} | Score: {p.score:.3f} | Factor: {p.decay_factor:.3f}")

if __name__ == "__main__":
    test_live_logic()
