#!/usr/bin/env python3
"""
Travel Logic v1.0
Fokus: Proaktiv assistance ved detekterede lokationsskift.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime, timezone
import geo_location_v7

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAVEL_STATE_FILE = os.path.join(_PROJECT_ROOT, "data/travel_state.json")

def check_for_travel():
    print("--- Travel Logic: Tjekker for geografiske skift ---")
    
    # 1. Hent nuværende lokation
    current_loc = geo_location_v7.get_current_location()
    current_city = current_loc.get('city', 'Unknown')
    
    # 2. Hent tidligere lokation
    last_city = "Unknown"
    if os.path.exists(TRAVEL_STATE_FILE):
        try:
            with open(TRAVEL_STATE_FILE, "r") as f:
                state = json.load(f)
                last_city = state.get("last_city", "Unknown")
        except:
            pass
            
    # 3. Analyser forskel
    if current_city != last_city and last_city != "Unknown":
        print(f"[TRAVEL]: Lokationsskift detekteret! {last_city} -> {current_city}")
        
        # Generer rejse-briefing
        briefing = {
            "event": "location_change",
            "from": last_city,
            "to": current_city,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "message": f"Velkommen til {current_city}. Jeg har opdateret dit vejr og din tidszone. Skal jeg finde lokale transportmuligheder eller de nærmeste kaffebarer til dine møder?"
        }
        
        # Gem ny state
        with open(TRAVEL_STATE_FILE, "w") as f:
            json.dump({"last_city": current_city, "last_update": briefing["timestamp"]}, f, indent=2)
            
        return briefing
    
    # Opdater state selvom ingen ændring (for initialisering)
    with open(TRAVEL_STATE_FILE, "w") as f:
        json.dump({"last_city": current_city, "last_update": datetime.now(timezone.utc).isoformat() + "Z"}, f, indent=2)
        
    return None

if __name__ == "__main__":
    # Test simulation: Sæt gammel by til noget andet
    if not os.path.exists(TRAVEL_STATE_FILE):
         with open(TRAVEL_STATE_FILE, "w") as f:
            json.dump({"last_city": "Aarhus"}, f)
        
    change = check_for_travel()
    if change:
        print(f"[BRIEFING]: {change['message']}")
    else:
        print("Ingen rejse detekteret (eller første kørsel).")
