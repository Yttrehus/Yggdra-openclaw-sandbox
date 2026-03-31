#!/usr/bin/env python3
"""
Time-to-Leave Calculator v1.0
Fokus: Beregning af afgangstidspunkt baseret på kalender, trafik og lokation.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime, timedelta, timezone
import geo_location_v7
import google_calendar_read

def calculate_ttl():
    print("--- Time-to-Leave: Analyserer dags-agenda ---")
    
    # 1. Hent lokation
    loc = geo_location_v7.get_current_location()
    
    # 2. Hent agenda
    agenda = google_calendar_read.get_todays_agenda()
    
    if not agenda:
        return None

    # Finder næste fysiske møde (Office)
    next_meeting = next((e for e in agenda if e['location'] == 'Office'), None)
    
    if not next_meeting:
        return None

    # Simulation af rejsetid (reelt Google Maps Distance Matrix API)
    travel_time_minutes = 25 
    traffic_buffer = 10
    total_prep_time = travel_time_minutes + traffic_buffer
    
    meeting_time_str = next_meeting['time']
    # Antager nutidig dato for simulation
    now = datetime.now()
    meeting_time = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {meeting_time_str}", "%Y-%m-%d %H:%M")
    
    leave_time = meeting_time - timedelta(minutes=total_prep_time)
    
    result = {
        "meeting": next_meeting['title'],
        "meeting_time": meeting_time_str,
        "travel_time": travel_time_minutes,
        "buffer": traffic_buffer,
        "leave_time": leave_time.strftime("%H:%M"),
        "location": next_meeting['location']
    }
    
    return result

if __name__ == "__main__":
    ttl = calculate_ttl()
    if ttl:
        print(f"[TTL]: For at nå '{ttl['meeting']}' kl. {ttl['meeting_time']} i {ttl['location']},")
        print(f"       skal du tage afsted senest kl. {ttl['leave_time']} (inkl. {ttl['buffer']} min buffer).")
    else:
        print("Ingen fysiske møder fundet der kræver TTL beregning.")
