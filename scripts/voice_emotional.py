"""
Voice Emotional Intelligence v1.2
Fokus: Tilpasning af stemmeleje og tone baseret på system-sundhed, lokation OG Vocal Sentiment.
Integration med V21.1 Neural Empathy.
"""
import os
import json

def get_emotional_tone(vocal_sentiment=None):
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

    # 3. Integrer Vocal Sentiment (V21.1)
    # Hvis brugeren er frustreret, skal assistenten være ekstra 'soft' og rolig.
    if vocal_sentiment and vocal_sentiment.get("state") == "Frustreret":
        return {
            "tone": "empathic_support",
            "pitch": "slightly_lower",
            "speed": "slower",
            "description": "Brugeren virker frustreret. Formidlingen er ekstra rolig, anerkendende og langsom for at de-eskalerer."
        }

    # 4. Beslut standard tone
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
    # Test med simuleret frustration
    mock_sentiment = {"state": "Frustreret", "confidence": 0.89}
    tone = get_emotional_tone(vocal_sentiment=mock_sentiment)
    print("--- Emotional Intelligence Analysis v1.2 (Integrated) ---")
    print(f"Detekteret tone: {tone['tone'].upper()}")
    print(f"Beskrivelse: {tone['description']}")
