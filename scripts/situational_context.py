#!/usr/bin/env python3
"""
Situational Context Engine v1.0
Fokus: Simulation af tids- og lokations-baserede triggere.
Del af Lag 5 (Situationsbevidsthed).
"""
import os
import json
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
CONTEXT_FILE = os.path.join(_PROJECT_ROOT, "data/situational_state.json")

def get_situational_trigger():
    # I en rigtig app ville dette hente GPS data eller kalender events
    # Her simulerer vi en "On the road" trigger (Rute 256 kontekst)
    
    hour = datetime.now().hour
    is_driving_time = 7 <= hour <= 9 or 15 <= hour <= 17
    
    if is_driving_time:
        return {
            "mode": "voice_only",
            "context": "driving",
            "recommendation": "Hold svarene korte (max 3 sætninger). Fokus på proaktiv status."
        }
    else:
        return {
            "mode": "multimodal",
            "context": "office",
            "recommendation": "Giv detaljerede svar og henvis til Notion visualiseringer."
        }

def save_state(state):
    with open(CONTEXT_FILE, "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    trigger = get_situational_trigger()
    print(f"--- Situational Trigger Detekteret ---")
    print(json.dumps(trigger, indent=2))
    save_state(trigger)
