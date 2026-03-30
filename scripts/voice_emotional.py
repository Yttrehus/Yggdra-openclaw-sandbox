#!/usr/bin/env python3
"""
Voice Emotional Intelligence v1.1
Fokus: Tilpasning af stemmeleje og tone baseret på system-sundhed OG lokation.
Nu med 'Casual/Soft' tone for home mode.
"""
import os
import json

def get_emotional_tone():
    # 1. Hent situatonal state (lokation)
    loc_context = "office"
    situational_file = "data/situational_state.json"
    if os.path.exists(situational_file):
        with open(situational_file, "r") as f:
            loc_context = json.load(f).get("context", "office")

    # 2. Hent system sundhed
    report_path = "data/maintenance_report.md"
    is_critical = False
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            content = f.read()
            if "[CRITICAL]" in content:
                is_critical = True

    # 3. Beslut tone
    if is_critical:
        return {
            "tone": "urgent",
            "pitch": "slightly_higher",
            "speed": "faster",
            "description": "Systemet er i alarmtilstand. Formidlingen skal være hurtig og præcis."
        }
    
    if loc_context == "home":
        return {
            "tone": "soft",
            "pitch": "slightly_lower",
            "speed": "slower",
            "description": "Brugeren er hjemme. Formidlingen er rolig, refleksiv og blød."
        }

    return {
        "tone": "calm",
        "pitch": "neutral",
        "speed": "natural",
        "description": "Alt kører perfekt. Formidlingen er professionel og støttende."
    }

if __name__ == "__main__":
    tone = get_emotional_tone()
    print("--- Emotional Intelligence Analysis v1.1 ---")
    print(f"Detekteret tone: {tone['tone'].upper()}")
    print(f"Beskrivelse: {tone['description']}")
