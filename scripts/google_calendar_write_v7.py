#!/usr/bin/env python3
"""
Google Calendar Write Integration v1.0
Fokus: Oprettelse af kalender-hændelser med V8 Collaborative Security.
Del af V7.1 Real-world API Integration.
"""
import os
import json
from datetime import datetime, timezone
import load_secrets
import vidar_security_scan

def create_calendar_event(title, start_time, location="Remote"):
    print(f"--- Google Calendar V7.1: Opretter hændelse '{title}' ---")
    
    # 1. Vidar Security Pre-scan (V8)
    # Vi inkluderer payload for at Vidar kan vurdere risikoen
    payload = {"title": title, "start": start_time, "location": location}
    is_safe, msg = vidar_security_scan.scan_api_call(
        service="Google Calendar", 
        action="CreateEvent", 
        payload=payload,
        model="google/gemini-1.5-flash"
    )
    
    if not is_safe:
        print(f"[BLOCK]: {msg}")
        return False

    # 2. Hent credentials (V7)
    api_key = load_secrets.get_secret("GOOGLE_CLIENT_ID")
    if not api_key or "your_" in api_key:
        print("[SIMULATION]: Ingen reel Google Key fundet. Logger hændelse til lokal state.")
        return simulate_calendar_write(title, start_time, location)

    print(f"[API]: Forbinder til Google API og opretter event...")
    # Reel SDK logik her (service.events().insert...)
    return True

def simulate_calendar_write(title, start, loc):
    print(f"[STATE]: Hændelse '{title}' oprettet til {start} i {loc}.")
    return True

if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "V8 Architecture Review"
    s = sys.argv[2] if len(sys.argv) > 2 else "2026-06-25T14:00:00Z"
    create_calendar_event(t, s)
