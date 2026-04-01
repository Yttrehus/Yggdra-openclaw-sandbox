#!/usr/bin/env python3
"""
Context-Aware Task Generator v1.0
Fokus: Automatisk generering af subtasks baseret på multi-modal kontekst.
Del af V7.5 Kognitiv Proaktivitet.
"""
import json
import os
from datetime import datetime, timezone
import task_breakdown
import geo_location_v7
import weather_context
import google_calendar_read

def analyze_context_and_generate_tasks():
    print("--- Context Task Generator: Analyserer Multi-Modal Kontekst ---")
    
    new_tasks = []
    
    # 1. Analyser Vejr
    weather_summary = weather_context.get_weather_summary()
    if "5.7 grader" in weather_summary or "regn" in weather_summary.lower():
        new_tasks.append("Husk varmt tøj til transport mellem møder (det er koldt)")
        
    # 2. Analyser Agenda
    agenda = google_calendar_read.get_todays_agenda()
    for event in agenda:
        if "Remote" in event.get("location", ""):
            new_tasks.append(f"Tjek mikrofon og kamera før '{event['title']}'")
        if "Office" in event.get("location", ""):
            new_tasks.append(f"Forbered noter til fysisk møde: {event['title']}")

    # 3. Analyser Rejse-kontekst (Flight awareness)
    import flight_aware_mock
    flight = flight_aware_mock.check_for_upcoming_flights()
    if flight and flight.get("arrival") == "EWR":
        new_tasks.append("Pak rejsetaske til New York turen i morgen")
        new_tasks.append("Tjek ind til fly SK909")

    if new_tasks:
        print(f"[GENERATOR]: Genereret {len(new_tasks)} kontekst-specifikke opgaver.")
        # Vi grupperer disse under et 'context_tasks' mål
        task_breakdown.breakdown_goal("context_guidance", new_tasks)
    else:
        print("[GENERATOR]: Ingen nye opgaver identificeret fra nuværende kontekst.")

if __name__ == "__main__":
    analyze_context_and_generate_tasks()
