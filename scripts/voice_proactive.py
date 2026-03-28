#!/usr/bin/env python3
"""
Voice Proactive System v1.2
Fokus: Generering af proaktive hilsner baseret på systemets situationsbevidsthed.
Nu med Confidence Metrics og Inactivity Triggers.
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

def get_memory_stats():
    """Beregner statistik for hukommelsens kvalitet."""
    if os.path.exists(FACTS_FILE):
        try:
            with open(FACTS_FILE, "r") as f:
                facts = json.load(f)
            
            if not facts:
                return 0, 0.0
            
            count = len(facts)
            confidences = [f.get('confidence', 0.0) for f in facts if 'confidence' in f]
            avg_conf = (sum(confidences) / len(confidences)) * 100 if confidences else 0.0
            
            return count, avg_conf
        except:
            return 0, 0.0
    return 0, 0.0

def check_project_inactivity():
    """Tjekker om vigtige projekter er 'stale'."""
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
    fact_count, avg_conf = get_memory_stats()
    inactivity = check_project_inactivity()
    situation = check_situational_mode()
    
    # Formater hilsen
    msg = f"{greeting}. {summary} "
    msg += f"Din hukommelse indeholder nu {fact_count} fakta med en gennemsnitlig pålidelighed på {avg_conf:.1f} procent. "
    if situation:
        msg += f"{situation} "
    msg += f"En vigtig bemærkning: {inactivity} Skal jeg give dig ugens overblik?"
    
    return msg

if __name__ == "__main__":
    print(f"--- Proaktiv Voice Greeting v1.2 ---")
    print(generate_greeting())
