#!/usr/bin/env python3
"""
Contextual Visual Generator Mock v1.1
Fokus: Simulation af billede-generering til display-enheder med Urgency Highlights.
Del af V7.2 Multi-Modal Context.
"""
import os
import json
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VISUAL_STATE_FILE = os.path.join(_PROJECT_ROOT, "data/visual_display_state.json")
MAINTENANCE_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")

def get_urgency_level():
    """Analyserer maintenance_report.md for at bestemme visuel urgency."""
    if not os.path.exists(MAINTENANCE_FILE):
        return "NORMAL", "green"
    
    with open(MAINTENANCE_FILE, "r") as f:
        content = f.read()
        
    if "[ERROR]" in content or "[CRITICAL]" in content:
        return "CRITICAL", "red"
    elif "[WARNING]" in content:
        return "WARNING", "yellow"
    
    return "NORMAL", "green"

def generate_dashboard_prompt():
    print("--- Visual Generator v1.1: Designer Dashboard Layout ---")
    
    # 1. Saml sundheds-kontekst (Urgency Highlights)
    status_label, status_color = get_urgency_level()
    print(f"[VISUAL]: Detekteret systemstatus: {status_label} ({status_color})")

    # 2. Saml miljø-kontekst
    import weather_context
    weather = weather_context.get_weather_summary()
    
    # 3. Saml tids-kontekst
    import google_calendar_read
    agenda = google_calendar_read.get_todays_agenda()
    
    # Design prompt til "Display"
    prompt = {
        "version": "1.1",
        "layout": "split-screen",
        "urgency_highlight": {
            "active": status_label != "NORMAL",
            "level": status_label,
            "color_hex": "#FF0000" if status_color == "red" else "#FFFF00",
            "animation": "pulse" if status_label == "CRITICAL" else "static"
        },
        "left_panel": {
            "title": "Weather & Environment",
            "content": weather,
            "theme": "dynamic-skyline"
        },
        "right_panel": {
            "title": "Today's Mission",
            "events": agenda,
            "theme": "cyber-notion"
        },
        "footer": {
            "system_status": f"Status: {status_label}",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    print(f"[VISUAL]: Genereret UI metadata for '{prompt['layout']}' layout med {status_label} highlight.")
    
    with open(VISUAL_STATE_FILE, "w") as f:
        json.dump(prompt, f, indent=2)
        
    return prompt

if __name__ == "__main__":
    generate_dashboard_prompt()
