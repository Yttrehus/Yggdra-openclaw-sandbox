#!/usr/bin/env python3
"""
Routine Engine v1.0
Fokus: Kontekstuelle anbefalinger baseret på tidspunkt og dagens agenda.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime
import pytz
import time_of_day_v7
import google_calendar_read

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIME_STATE_FILE = os.path.join(_PROJECT_ROOT, "data/time_state.json")

def get_routine_suggestion():
    # 1. Hent tidspunkt (V7.2)
    greeting = time_of_day_v7.get_time_of_day_greeting()
    
    # 2. Hent agenda
    agenda = google_calendar_read.get_todays_agenda()
    
    # 3. Logik for anbefalinger
    if greeting == "Godmorgen":
        if agenda:
            return "Da du har en tætpakket dag, foreslår jeg at vi starter med en kort gennemgang af de mest kritiske subtasks nu. "
        else:
            return "Da din kalender er tom, er det en perfekt mulighed for at fokusere på dybt arbejde i V7 arkitekturen. "
            
    elif greeting == "Godaften":
        return "Skal vi lave en hurtig opsummering af dagens fremskridt og opdatere din TRIAGE for i morgen? "
        
    return ""

if __name__ == "__main__":
    print(get_routine_suggestion())
