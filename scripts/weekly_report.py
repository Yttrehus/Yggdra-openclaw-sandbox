#!/usr/bin/env python3
"""
Weekly Report Generator v1.2
Fokus: Opsummering af ugens faktuelle viden og system-performance.
Nu med Confidence-tracking og kvalitets-visualisering.
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
    print("--- Genererer Ugentlig Rapport v1.2 ---")
    facts = load_data(FACTS_FILE)
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    
    # Filtrer fakta fra den sidste uge
    weekly_facts = []
    all_confidences = []
    weekly_confidences = []
    
    for f in facts:
        try:
            conf = f.get('confidence', 0.0)
            all_confidences.append(conf)
            
            dt = datetime.fromisoformat(f.get('timestamp', ''))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            
            if dt > one_week_ago:
                weekly_facts.append(f)
                weekly_confidences.append(conf)
        except Exception:
            continue
            
    # Beregn statistikker
    avg_total_conf = (sum(all_confidences) / len(all_confidences)) * 100 if all_confidences else 0.0
    avg_weekly_conf = (sum(weekly_confidences) / len(weekly_confidences)) * 100 if weekly_confidences else 0.0
    
    # Check downtime
    missing_days = check_pipeline_continuity(7)
    
    # Opret rapport-mappe hvis den ikke findes
    os.makedirs(REPORT_PATH, exist_ok=True)
    
    filename = f"report_{now.strftime('%Y-W%V')}.md"
    filepath = os.path.join(REPORT_PATH, filename)
    
    with open(filepath, "w") as f:
        f.write(f"# Yggdra Ugentlig Rapport - {now.strftime('%Y, Uge %V')}\n\n")
        
        f.write("## 📊 Hukommelsens Kvalitet (Lag 2)\n")
        f.write(f"- **Gennemsnitlig pålidelighed (total):** {avg_total_conf:.1f}%\n")
        if weekly_facts:
            f.write(f"- **Pålidelighed for ugens læringer:** {avg_weekly_conf:.1f}%\n")
        f.write(f"- **Antal validerede fakta:** {len(facts)}\n\n")

        f.write("## 🧠 Nye Læringer (Sidste 7 dage)\n")
        if weekly_facts:
            for fact in weekly_facts:
                conf_stars = "⭐" * int(fact.get('confidence', 0) * 5)
                f.write(f"- {fact['fact']} {conf_stars} *(Kilde: {fact.get('source_date', 'Ukendt')})*\n")
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
