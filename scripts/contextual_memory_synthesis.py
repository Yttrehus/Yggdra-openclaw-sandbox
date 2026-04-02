#!/usr/bin/env python3
"""
Contextual Memory Synthesis v1.0
Fokus: Opsummering af dags-agenda og projekter til langtids-fakta.
Del af V7.6 Contextual Memory Synthesis.
"""
import json
import os
from datetime import datetime, timezone
import google_calendar_read
import notion_read_projects

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")

def synthesize_daily_context():
    print("--- Memory Synthesis: Destillerer dags-kontekst til langtids-hukommelse ---")
    
    # 1. Hent dags-data
    agenda = google_calendar_read.get_todays_agenda()
    projects = notion_read_projects.get_active_projects()
    
    new_facts = []
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    
    # 2. Udled fakta fra agenda
    if agenda:
        event_titles = [e['title'] for e in agenda]
        fact = {
            "fact": f"Dags-agenda fokuseret på: {', '.join(event_titles)}.",
            "confidence": 0.9,
            "timestamp": timestamp,
            "source": "Google Calendar Synthesis"
        }
        new_facts.append(fact)
        
    # 3. Udled fakta fra Notion
    p0 = [p['name'] for p in projects if p.get('priority') == 'P0']
    if p0:
        fact = {
            "fact": f"Primært strategisk fokus er projektet '{p0[0]}'.",
            "confidence": 0.95,
            "timestamp": timestamp,
            "source": "Notion Synthesis"
        }
        new_facts.append(fact)

    # 4. Gem til extracted_facts.json
    if new_facts:
        existing_facts = []
        if os.path.exists(FACTS_FILE):
            with open(FACTS_FILE, "r") as f:
                existing_facts = json.load(f)
        
        existing_facts.extend(new_facts)
        
        with open(FACTS_FILE, "w") as f:
            json.dump(existing_facts, f, indent=2)
            
        print(f"[SUCCESS]: Syntetiseret {len(new_facts)} nye fakta til hukommelsen.")
        return new_facts
    
    return []

if __name__ == "__main__":
    synthesize_daily_context()
