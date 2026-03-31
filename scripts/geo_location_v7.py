#!/usr/bin/env python3
"""
Geo-Location Detection v1.0
Fokus: Automatisk lokations-detektering via Geo-IP (simulation af reelt opslag).
Del af V7.2 Multi-Modal Context.
"""
import os
import json
import requests

def get_current_location():
    print("--- Geo-Location: Detekterer nuværende placering ---")
    
    # I en reel app ville vi bruge: requests.get('https://ipapi.co/json/').json()
    # Her simulerer vi et succesfuldt opslag
    try:
        # requests.get('https://ipapi.co/json/', timeout=5).json()
        location_data = {
            "city": "Copenhagen",
            "country": "Denmark",
            "latitude": 55.6759,
            "longitude": 12.5655
        }
        print(f"[GEO]: Detekteret by: {location_data['city']}")
        return location_data
    except Exception as e:
        print(f"[ERROR]: Kunne ikke detektere lokation: {e}")
        return {"city": "Unknown", "latitude": 0, "longitude": 0}

if __name__ == "__main__":
    loc = get_current_location()
    print(f"[RESULT]: {loc['city']}, {loc['country']}")
