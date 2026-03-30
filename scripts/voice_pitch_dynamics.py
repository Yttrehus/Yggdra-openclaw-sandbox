#!/usr/bin/env python3
"""
Voice Pitch Dynamics v1.0
Fokus: Simulation af emotionel betoning (pitch shifts) baseret på informationstype.
Del af V6.4 Oplevelses-evolution.
"""
import json

def get_pitch_style(text):
    """Analyserer tekst og returnerer en pitch-profil til simulator."""
    # Prioriteter: Urgent > Positive > Neutral
    urgent_keywords = ["fejl", "advarsel", "critical", "blocking", "stop", "stagnant"]
    positive_keywords = ["succes", "fuldført", "mål", "progress", "fremdrift", "perfekt"]
    
    lowered_text = text.lower()
    
    if any(k in lowered_text for k in urgent_keywords):
        return {
            "style": "URGENT",
            "pitch": "+5%",
            "stability": "lower",
            "clarity": "high",
            "description": "Højere pitch og intensitet for at signalere behov for opmærksomhed."
        }
    elif any(k in lowered_text for k in positive_keywords):
        return {
            "style": "POSITIVE",
            "pitch": "+2%",
            "stability": "higher",
            "clarity": "medium",
            "description": "Let løftet pitch og høj stabilitet for at fejre fremdrift."
        }
    else:
        return {
            "style": "NEUTRAL",
            "pitch": "0%",
            "stability": "normal",
            "clarity": "normal",
            "description": "Standard professionel betoning."
        }

if __name__ == "__main__":
    test_cases = [
        "Vi har opnået stor succes med V6 integrationen!",
        "Der er en kritisk fejl i systemets hukommelse.",
        "Jeg har opdateret din kalender med et nyt møde."
    ]
    
    for t in test_cases:
        p = get_pitch_style(t)
        print(f"[TEXT]: {t}")
        print(f"[PITCH PROFILE]: {p['style']} (Pitch: {p['pitch']}, Stability: {p['stability']})")
        print("-" * 20)
