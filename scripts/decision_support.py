#!/usr/bin/env python3
"""
Decision Support v1.0
Fokus: Proaktiv foreslåelse af beslutninger baseret på systemrapporter.
Del af V6.3 Kognitiv Guidance.
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAINTENANCE_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")
DECISIONS_LOG = os.path.join(_PROJECT_ROOT, "data/proposed_decisions.json")

def analyze_and_propose():
    proposals = []
    
    # 1. Tjek system sundhed (Maintenance)
    if os.path.exists(MAINTENANCE_FILE):
        with open(MAINTENANCE_FILE, "r") as f:
            content = f.read()
            if "Qdrant disk space lav" in content:
                proposals.append({
                    "id": "purge_old_logs",
                    "title": "Purge af forældede logfiler",
                    "reason": "Qdrant diskplads er på 85%. En purge af data ældre end 90 dage vil frigøre 15GB.",
                    "action": "scripts/purge_logs.sh --days 90",
                    "risk_level": "low"
                })

    # 2. Tjek strategisk fremdrift (Goals)
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            goals = json.load(f)
            v6_goal = next((g for g in goals if g["id"] == "v6_completion"), None)
            if v6_goal and v6_goal["progress"] < 30:
                proposals.append({
                    "id": "shift_focus_v6",
                    "title": "Intensiver V6 Arkitektur Sprint",
                    "reason": "Fremdriften på V6 er under 30%. Jeg foreslår at vi de-prioriterer research i 48 timer.",
                    "action": "scripts/triage_update.py --focus v6",
                    "risk_level": "high"
                })

    if proposals:
        with open(DECISIONS_LOG, "w") as f:
            json.dump({"proposals": proposals, "timestamp": datetime.now().isoformat()}, f, indent=2)
    
    return proposals

if __name__ == "__main__":
    found = analyze_and_propose()
    for p in found:
        print(f"[PROPOSAL]: {p['title']} - Grund: {p['reason']}")
