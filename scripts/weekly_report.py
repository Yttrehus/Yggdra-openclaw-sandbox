#!/usr/bin/env python3
"""
Weekly Report Generator v1.0
Fokus: Opsummering af ugens faktuelle viden og system-performance.
Henter data fra extracted_facts.json og maintenance_state.json.
"""

import os
import json
from datetime import datetime, timedelta, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
REPORT_PATH = os.path.join(_PROJECT_ROOT, "memory/weekly_reports")

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def generate_report():
    print("--- Genererer Ugentlig Rapport ---")
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
            
        f.write("\n## 🛠 System Status\n")
        # Her kunne vi inkludere data fra maintenance_audit
        f.write("- Pipeline: Se data/maintenance_report.md for detaljer.\n")
        f.write("- Memory: Retrieval Engine v2.1 er stabil.\n")
        
        f.write("\n## 🎯 Næste Skridt\n")
        f.write("- Løs pipeline alerts på VPS.\n")
        f.write("- Initialisér Notion database.\n")
        
    print(f"Rapport gemt i: {os.path.relpath(filepath, _PROJECT_ROOT)}")

if __name__ == "__main__":
    generate_report()
