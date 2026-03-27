#!/usr/bin/env python3
"""
Rescan Prompt Generator v1.0
Analyserer pipeline downtime og genererer en LLM prompt til at genoprette videns-hullerne.
"""
import os
import json
from datetime import datetime, timedelta, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTELLIGENCE_DIR = os.path.join(_PROJECT_ROOT, "data/intelligence")

def get_missing_dates(days=7):
    missing = []
    now = datetime.now(timezone.utc)
    for i in range(days):
        date_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        if not os.path.exists(os.path.join(INTELLIGENCE_DIR, f"daily_{date_str}.md")):
            missing.append(date_str)
    return sorted(missing)

def generate_prompt():
    missing = get_missing_dates()
    if not missing:
        print("Ingen huller i hukommelsen detekteret.")
        return

    print(f"--- Genererer Rescan Prompt for {len(missing)} manglende dage ---")
    
    prompt = f"""# RE-SCAN MISSION: LUKNING AF VIDENS-GAB

Vi har haft et pipeline-nedbrud i følgende periode: {missing[0]} til {missing[-1]}.
Dette har efterladt huller i vores epistemiske fundament.

## DIN OPGAVE:
Foretag en fokuseret søgning og ekstraktion af de vigtigste hændelser og tekniske gennembrud for hver af disse specifikke datoer:
{', '.join(missing)}

## KRAV:
1. Fokus på: AI-arkitekturer, LLM-landskab (Anthropic, Google, OpenAI), og nye automation patterns.
2. Format: Dokumentér dine fund i `data/intelligence/daily_YYYY-MM-DD.md` for hver dato.
3. Kvalitet: Overhold APA 7th standarden for kildehenvisninger.

Målet er at genoprette systemets situationsbevidsthed (Lag 5) før vi ruller V5-feature pakken ud.
"""
    
    output_path = os.path.join(_PROJECT_ROOT, "0_backlog/RESCAN_MISSION.md")
    with open(output_path, "w") as f:
        f.write(prompt)
    
    print(f"Mission-brief gemt i: {os.path.relpath(output_path, _PROJECT_ROOT)}")

if __name__ == "__main__":
    generate_prompt()
