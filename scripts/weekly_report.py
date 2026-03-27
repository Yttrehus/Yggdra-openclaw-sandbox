#!/usr/bin/env python3
"""
Weekly Report Generator v1.1
Fokus: Opsummering af ugens faktuelle viden og system-performance.
Nu med overvågning af pipeline downtime.
"""

import os
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
INTELLIGENCE_DIR = os.path.join(_PROJECT_ROOT, "data/intelligence")
REPORT_PATH = os.path.join(_PROJECT_ROOT, "memory/weekly_reports")

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def check_pipeline_continuity(days=7):
    """Tæller hvor mange daglige filer der mangler i den sidste uge."""
    missing_count = 0
    now = datetime.now(timezone.utc)
    for i in range(days):
        date_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        path = Path(INTELLIGENCE_DIR) / f"daily_{date_str}.md"
        if not path.exists():
            missing_count += 1
    return missing_count

def generate_report():
    print("--- Genererer Ugentlig Rapport v1.1 ---")
    facts = load_data(FACTS_FILE)
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    
    # Filtrer fakta fra den sidste uge
    weekly_facts = []
    for f in facts:
        try:
            dt = datetime.fromisoformat(f.get('timestamp', ''))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt > one_week_ago:
                weekly_facts.append(f)
        except Exception:
            continue
            
    # Check downtime
    missing_days = check_pipeline_continuity(7)
    
    # Opret rapport-mappe hvis den ikke findes
    os.makedirs(REPORT_PATH, exist_ok=True)
    
    filename = f"report_{now.strftime('%Y-W%V')}.md"
    filepath = os.path.join(REPORT_PATH, filename)
    
    with open(filepath, "w") as f:
        f.write(f"# Yggdra Ugentlig Rapport - {now.strftime('%Y, Uge %V')}\n\n")
        
        f.write("## 🧠 Nye Læringer (Sidste 7 dage)\n")
        if weekly_facts:
            for fact in weekly_facts:
                f.write(f"- {fact['fact']} *(Kilde: {fact.get('source_date', 'Ukendt')})*\n")
        else:
            f.write("Ingen nye fakta udtrukket i denne uge.\n")
            
        f.write("\n## 🛠 System Sundhed & Kontinuitet\n")
        if missing_days > 0:
            status_text = "⚠️ PIPELINE DOWNTIME DETEKTERET"
            f.write(f"- **Status:** {status_text}\n")
            f.write(f"- **Manglende dage:** {missing_days} ud af de sidste 7 dage.\n")
            f.write("- **Anbefaling:** Følg `04.VPS_RECOVERY_GUIDE.md` straks.\n")
        else:
            f.write("- **Status:** ✅ Alle systemer kører optimalt.\n")
            f.write("- **Kontinuitet:** 100% (7/7 dage dækket).\n")
        
        f.write("\n## 🎯 Næste Skridt\n")
        if missing_days > 0:
            f.write("- **PRIORITET:** Genopret VPS videns-flow.\n")
        f.write("- Vedligehold `LIB.research` evergreen status.\n")
        f.write("- Forbered V5 Situationsbevidsthed udrulning.\n")
        
    print(f"Rapport gemt i: {os.path.relpath(filepath, _PROJECT_ROOT)}")

if __name__ == "__main__":
    generate_report()
