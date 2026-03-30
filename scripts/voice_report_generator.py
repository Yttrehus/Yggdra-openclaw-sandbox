#!/usr/bin/env python3
"""
Voice Report Generator v1.0
Fokus: Generering af komplekse, men mundrette statusrapporter til voice-interfacet.
Del af Lag 5 (Situationsbevidsthed).
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")
DRIFT_FILE = os.path.join(_PROJECT_ROOT, "data/drift_status.json")
MAINTENANCE_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")

def generate_voice_report():
    report_chunks = []
    
    # 1. Overordnet strategisk status
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            goals = json.load(f)
            v6_goal = next((g for g in goals if g["id"] == "v6_completion"), None)
            if v6_goal:
                report_chunks.append(f"Vi er nået {v6_goal['progress']} procent i mål med V6 arkitekturen.")

    # 2. Sundhedstjek (Drift & Maintenance)
    drift_ok = True
    if os.path.exists(DRIFT_FILE):
        with open(DRIFT_FILE, "r") as f:
            drift = json.load(f)
            if "DRIFT DETECTED" in drift.get("status", ""):
                report_chunks.append("Jeg bemærker dog, at vores backlog er ved at blive forældet.")
                drift_ok = False
    
    if os.path.exists(MAINTENANCE_FILE):
        with open(MAINTENANCE_FILE, "r") as f:
            content = f.read()
            if "WARNING" in content or "ERROR" in content:
                report_chunks.append("Der er også et par kritiske systemfejl, der kræver din opmærksomhed.")

    # 3. Konklusion
    if drift_ok:
        report_chunks.append("Alt i alt kører vi efter planen.")
    else:
        report_chunks.append("Vi bør prioritere en oprydning i vores triage, før vi fortsætter.")

    return " ".join(report_chunks)

if __name__ == "__main__":
    print(generate_voice_report())
