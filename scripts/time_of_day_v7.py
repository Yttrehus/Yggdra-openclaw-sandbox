#!/usr/bin/env python3
"""
Time of Day Analysis v1.0
Fokus: Dynamisk hilsen baseret på lokal tid og tidszone.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime
import pytz

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIME_STATE_FILE = os.path.join(_PROJECT_ROOT, "data/time_state.json")

def get_time_of_day_greeting():
    # 1. Hent synkroniseret tid (hvis tilgængelig)
    if os.path.exists(TIME_STATE_FILE):
        with open(TIME_STATE_FILE, "r") as f:
            state = json.load(f)
            tz_name = state.get("timezone", "UTC")
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
    else:
        now = datetime.now()
    
    hour = now.hour
    
    if 5 <= hour < 12:
        return "Godmorgen"
    elif 12 <= hour < 18:
        return "Goddag"
    elif 18 <= hour < 23:
        return "Godaften"
    else:
        return "Godnat"

if __name__ == "__main__":
    print(get_time_of_day_greeting())
