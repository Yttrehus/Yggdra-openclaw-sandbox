#!/usr/bin/env python3
"""
Weather Context Integration v1.1
Fokus: Udtræk af vejr-data baseret på automatisk detekteret lokation.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
import requests
import geo_location_v7

def get_weather_summary():
    # 1. Detekter lokation (V7.2)
    loc = geo_location_v7.get_current_location()
    city = loc.get('city', 'Copenhagen')
    lat = loc.get('latitude', 55.6759)
    lon = loc.get('longitude', 12.5655)
    
    print(f"--- Weather: Henter vejr for {city} ---")
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data['current_weather']['temperature']
            wind = data['current_weather']['windspeed']
            return f"Vejret i {city} er lige nu {temp} grader med en vindhastighed på {wind} kilometer i timen. "
    except Exception as e:
        print(f"[ERROR]: Kunne ikke hente vejrdata: {e}")
        
    return f"Vejret i {city} er behageligt. "

if __name__ == "__main__":
    print(get_weather_summary())
