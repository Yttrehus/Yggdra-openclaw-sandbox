#!/usr/bin/env python3
"""
Action Engine Mock v1.0
Fokus: Simulation af handlinger baseret på autentificerede tokens.
Tema: Læsning og skrivning til Google Calendar.
"""
import time
import json
from datetime import datetime, timedelta

def load_mock_tokens():
    # I en rigtig app ville dette læse fra data/secrets/
    return {"access_token": "mock_access_abc123", "scope": ["calendar.readonly", "calendar.events"]}

def action_read_calendar():
    tokens = load_mock_tokens()
    print(f"[ACTION ENGINE]: Bruger token {tokens['access_token'][:6]}... til at læse kalender.")
    time.sleep(1.0)
    # Simulerer fundne events
    events = [
        {"summary": "Morgenmad", "start": "2026-03-31T08:00:00Z"},
        {"summary": "Yggdra Deep Work", "start": "2026-03-31T10:00:00Z"}
    ]
    print(f"[ACTION ENGINE]: Hentet {len(events)} events.")
    return events

def action_create_event(summary, start_time):
    tokens = load_mock_tokens()
    print(f"[ACTION ENGINE]: Bruger token {tokens['access_token'][:6]}... til at oprette event: {summary}")
    time.sleep(1.5)
    print(f"[ACTION ENGINE]: SUCCESS: Event '{summary}' oprettet til {start_time}")
    return True

if __name__ == "__main__":
    print("--- Action Engine Workflow Simulation ---")
    
    # 1. Læs
    current_events = action_read_calendar()
    
    # 2. Beslut (Simulation af logik)
    print("\n[LOGIK]: Ingen konflikter fundet for i morgen kl. 14.")
    
    # 3. Skriv
    new_event_start = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT14:00:00Z")
    action_create_event("V6 Arkitektur Sprint", new_event_start)
