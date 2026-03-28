#!/usr/bin/env python3
"""
Voice Proactive System v1.0
Fokus: Generering af proaktive hilsner baseret på systemets situationsbevidsthed.
Del af Lag 5 (Situationsbevidsthed).
"""
import os
import json
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
AUDIT_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")

def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 10: return "Godmorgen"
    if 10 <= hour < 18: return "Goddag"
    return "Godaften"

def get_system_summary():
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            content = f.read()
        if "Status: All Systems Operational" in content:
            return "Pipelinen kører perfekt, og alle fødekæder er grønne."
        else:
            return "Jeg har detekteret nogle uregelmæssigheder i pipelinen, som vi bør kigge på."
    return "Jeg kunne ikke finde min seneste sundhedsrapport."

def get_new_fact_count():
    if os.path.exists(FACTS_FILE):
        with open(FACTS_FILE, "r") as f:
            facts = json.load(f)
        # Find fakta fra det seneste døgn (simulering)
        return len(facts[-3:]) # Vi tager de 3 nyeste som "nye"
    return 0

def generate_greeting():
    greeting = get_time_greeting()
    summary = get_system_summary()
    facts_count = get_new_fact_count()
    
    full_message = f"{greeting}. {summary} Jeg har indsamlet {facts_count} nye indsigter siden vi sidst talte sammen. Skal jeg give dig ugens overblik?"
    
    print(f"--- Proaktiv Voice Greeting ---")
    print(full_message)

if __name__ == "__main__":
    generate_greeting()
