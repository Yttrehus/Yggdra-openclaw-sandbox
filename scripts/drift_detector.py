#!/usr/bin/env python3
"""
Drift Detector v1.0
Fokus: Overvågning af backlog-friskhed og identifikation af forældet status.
Del af V6.1 Hukommelses-evolution.
"""
import os
import time
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAGE_FILE = os.path.join(_PROJECT_ROOT, "0_backlog/TRIAGE.md")

def check_drift(max_days=7):
    if not os.path.exists(TRIAGE_FILE):
        return "Warning: TRIAGE.md missing."
    
    mtime = os.path.getmtime(TRIAGE_FILE)
    last_modified = datetime.fromtimestamp(mtime)
    days_since_update = (datetime.now() - last_modified).days
    
    if days_since_update > max_days:
        return f"DRIFT DETECTED: TRIAGE.md has not been updated in {days_since_update} days. Backlog may be stale."
    
    return f"Freshness OK: Last update {days_since_update} days ago."

if __name__ == "__main__":
    result = check_drift()
    print(result)
    
    # Skriv resultat til en midlertidig fil som voice_simulator kan læse
    with open(os.path.join(_PROJECT_ROOT, "data/drift_status.json"), "w") as f:
        import json
        json.dump({"status": result, "timestamp": datetime.now().isoformat()}, f)
