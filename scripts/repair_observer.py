#!/usr/bin/env python3
"""
Repair Observer v1.0
Fokus: Overvågning af færdiggjorte system_health opgaver og triggering af re-sweeps.
Del af V6.2 Handling & Eksekvering.
"""
import json
import os
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_FILE = os.path.join(_PROJECT_ROOT, "data/subtasks.json")
OBSERVER_STATE = os.path.join(_PROJECT_ROOT, "data/repair_observer_state.json")

def check_for_completed_repairs():
    if not os.path.exists(TASKS_FILE):
        return False

    with open(TASKS_FILE, "r") as f:
        all_tasks = json.load(f)

    if "system_health" not in all_tasks:
        return False

    completed_repairs = [t for t in all_tasks["system_health"] if t["status"] == "completed"]
    
    if not completed_repairs:
        return False

    # Tjek mod tidligere state for at undgå redundante sweeps
    last_count = 0
    if os.path.exists(OBSERVER_STATE):
        with open(OBSERVER_STATE, "r") as f:
            state = json.load(f)
            last_count = state.get("completed_count", 0)

    current_count = len(completed_repairs)
    
    if current_count > last_count:
        print(f"[REPAIR OBSERVER]: {current_count - last_count} nye system rettelser detekteret.")
        # Opdater state
        with open(OBSERVER_STATE, "w") as f:
            json.dump({"completed_count": current_count, "last_trigger": datetime.now(timezone.utc).isoformat()}, f)
        return True

    return False

def trigger_maintenance_sweep():
    print("[REPAIR OBSERVER]: Triggering automatisk maintenance sweep...")
    # I en reel app ville vi køre: os.system("python3 scripts/daily_sweep.py")
    # For denne PoC simulerer vi en succesfuld re-evaluering
    print("[REPAIR OBSERVER]: Sweep fuldført. System sundhed re-evalueret.")

if __name__ == "__main__":
    if check_for_completed_repairs():
        trigger_maintenance_sweep()
    else:
        print("[REPAIR OBSERVER]: Ingen nye rettelser kræver handling.")
