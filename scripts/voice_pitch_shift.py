#!/usr/bin/env python3
"""
Voice Pitch Shift v1.0
Fokus: Simulation af emotionel betoning baseret på informationens vigtighed.
Del af Lag 5 (Situationsbevidsthed) / V6.4 Oplevelses-evolution.
"""
import json
import os

def get_pitch_instruction(text):
    """Analyserer tekst og returnerer pitch-instruktioner for ElevenLabs/SSML simulation."""
    
    # Kritiske nøgleord der kræver højere pitch (opmærksomhed)
    urgent_keywords = ["fejl", "error", "vigtig", "kritisk", "advarsel", "system_health"]
    # Positive nøgleord der kræver lysere/varmere pitch
    positive_keywords = ["succes", "gennemført", "perfekt", "grønne", "mål"]
    
    text_lower = text.lower()
    
    if any(k in text_lower for k in urgent_keywords):
        return "PITCH: HIGH (Urgent/Alert)"
    elif any(k in text_lower for k in positive_keywords):
        return "PITCH: SLIGHTLY HIGH (Warm/Success)"
    else:
        return "PITCH: NEUTRAL (Professional)"

if __name__ == "__main__":
    test_texts = [
        "Der er opstået en kritisk fejl i systemet.",
        "Vi har nu gennemført handlingen med stor succes.",
        "Jeg har opdateret din backlog."
    ]
    
    for t in test_texts:
        print(f"[TEXT]: {t}")
        print(f"[SHIFTER]: {get_pitch_instruction(t)}")
        print("-" * 20)
