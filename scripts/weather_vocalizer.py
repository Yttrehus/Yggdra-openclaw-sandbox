#!/usr/bin/env python3
"""
Weather Vocalizer v1.0
Fokus: Integration af vejr-data i voice-interfacet.
Del af V7.2 Multi-Modal Context.
"""
import weather_context

def get_weather_vocalized():
    try:
        return weather_context.get_weather_summary()
    except:
        return ""

if __name__ == "__main__":
    print(get_weather_vocalized())
