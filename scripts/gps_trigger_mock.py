#!/usr/bin/env python3
"""
GPS Trigger Mock v1.0
Fokus: Simulation af geografiske hændelser der påvirker systemets tilstand.
Del af Lag 5 (Situationsbevidsthed).
"""
import time
import json
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITUATIONAL_FILE = os.path.join(_PROJECT_ROOT, "data/situational_state.json")

def simulate_gps_move(location_name):
    print(f"--- GPS Event: Bruger ankommer til '{location_name}' ---")
    
    if location_name == "home":
        state = {
            "mode": "casual",
            "context": "home",
            "location": "home",
            "recommendation": "Fokus på ugerapporter og refleksion. Undgå teknisk overload."
        }
    elif location_name == "office":
        state = {
            "mode": "multimodal",
            "context": "office",
            "location": "office",
            "recommendation": "Giv detaljerede svar og henvis til Notion visualiseringer."
        }
    else:
        state = {
            "mode": "voice_only",
            "context": "driving",
            "location": "unknown",
            "recommendation": "Hold svarene korte (max 3 sætninger)."
        }

    with open(SITUATIONAL_FILE, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"[GPS]: Situational state opdateret for {location_name}.")
    return state

if __name__ == "__main__":
    import sys
    loc = sys.argv[1] if len(sys.argv) > 1 else "home"
    simulate_gps_move(loc)
