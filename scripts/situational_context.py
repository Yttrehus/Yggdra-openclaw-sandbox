#!/usr/bin/env python3
"""
Situational Context Engine v1.1
Fokus: Simulation af tids-, lokations- og kalender-baserede triggere.
Nu med lokations-mocking for "Home" vs "Work".
Del af Lag 5 (Situationsbevidsthed).
"""
import os
import json
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
CONTEXT_FILE = os.path.join(_PROJECT_ROOT, "data/situational_state.json")

def get_situational_trigger(mock_location=None):
    # Tidstjek
    hour = datetime.now().hour
    is_driving_time = 7 <= hour <= 9 or 15 <= hour <= 17
    
    # Lokationstjek (Mocked)
    location = mock_location or "office" # Default
    
    if is_driving_time:
        return {
            "mode": "voice_only",
            "context": "driving",
            "location": location,
            "recommendation": "Hold svarene korte (max 3 sætninger). Fokus på proaktiv status."
        }
    elif location == "home":
        return {
            "mode": "casual",
            "context": "home",
            "location": "home",
            "recommendation": "Fokus på ugerapporter og refleksion. Undgå teknisk overload."
        }
    else:
        return {
            "mode": "multimodal",
            "context": "office",
            "location": "office",
            "recommendation": "Giv detaljerede svar og henvis til Notion visualiseringer."
        }

def save_state(state):
    with open(CONTEXT_FILE, "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    import sys
    loc = sys.argv[1] if len(sys.argv) > 1 else None
    trigger = get_situational_trigger(loc)
    print(f"--- Situational Trigger Detekteret ---")
    print(json.dumps(trigger, indent=2))
    save_state(trigger)
