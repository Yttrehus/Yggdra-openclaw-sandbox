#!/usr/bin/env python3
"""
Agenda Vocalizer v1.0
Fokus: Transformering af dags-agenda til mundret tekst til voice-interfacet.
Del af V7.1 Real-world API Integration.
"""
import json
import os
import google_calendar_read

def get_agenda_vocalized():
    agenda = google_calendar_read.get_todays_agenda()
    
    if not agenda:
        return "Din kalender ser tom ud for i dag. "
    
    count = len(agenda)
    intro = f"Du har {count} hændelser planlagt i dag. "
    
    events_text = []
    for event in agenda:
        events_text.append(f"Klokken {event['time']} har du {event['title']} i {event['location']}. ")
    
    return intro + "".join(events_text)

if __name__ == "__main__":
    print(get_agenda_vocalized())
