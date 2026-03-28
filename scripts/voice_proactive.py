#!/usr/bin/env python3
"""
Voice Proactive System v1.1
Fokus: Generering af proaktive hilsner baseret på systemets situationsbevidsthed.
Nu med Inactivity Triggers.
"""
import os
import json
from datetime import datetime, timezone, timedelta

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
        try:
            with open(FACTS_FILE, "r") as f:
                facts = json.load(f)
            return len(facts[-3:]) # Vi tager de 3 nyeste som "nye"
        except:
            return 0
    return 0

def check_project_inactivity():
    """Tjekker om vigtige projekter er 'stale'."""
    # Simpelt proaktivt tip baseret på nuværende prioriteter
    return "Vi har genoprettet 7 dages data, men vi mangler stadig at initialisere Notion."

def check_situational_mode():
    """Henter anbefaling baseret på situations-trigger (f.eks. kørsel)."""
    try:
        with open(os.path.join(_PROJECT_ROOT, "data/situational_state.json"), "r") as f:
            state = json.load(f)
            return f"Jeg bemærker du er i {state['context']} mode. {state['recommendation']}"
    except:
        return ""

def generate_greeting():
    greeting = get_time_greeting()
    summary = get_system_summary()
    facts_count = get_new_fact_count()
    inactivity = check_project_inactivity()
    situation = check_situational_mode()
    
    full_message = f"{greeting}. {summary} Jeg har indsamlet {facts_count} nye indsigter siden sidst. {situation} En vigtig bemærkning: {inactivity} Skal jeg give dig ugens overblik?"
    return full_message

if __name__ == "__main__":
    print(f"--- Proaktiv Voice Greeting v1.1 ---")
    print(generate_greeting())
