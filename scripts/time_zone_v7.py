#!/usr/bin/env python3
"""
Timezone Sync v1.0
Fokus: Automatisk tidszone-skift baseret på Geo-Location.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime
import pytz
import geo_location_v7

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIME_STATE_FILE = os.path.join(_PROJECT_ROOT, "data/time_state.json")

def sync_timezone():
    print("--- Timezone Sync: Tjekker lokal tid ---")
    
    # 1. Hent detekteret by
    loc = geo_location_v7.get_current_location()
    city = loc.get('city', 'Copenhagen')
    
    # 2. Map by til tidszone (simuleret opslag)
    # I en reel app: timezonefinder eller en API
    tz_map = {
        "Copenhagen": "Europe/Copenhagen",
        "New York": "America/New_York",
        "Tokyo": "Asia/Tokyo",
        "London": "Europe/London"
    }
    
    tz_name = tz_map.get(city, "UTC")
    tz = pytz.timezone(tz_name)
    local_time = datetime.now(tz)
    
    print(f"[TIME]: Synkroniseret til {tz_name}. Lokal tid er {local_time.strftime('%H:%M')}.")
    
    state = {
        "timezone": tz_name,
        "local_time": local_time.strftime("%H:%M"),
        "city": city,
        "last_sync": datetime.now().isoformat()
    }
    
    with open(TIME_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
        
    return state

if __name__ == "__main__":
    sync_timezone()
