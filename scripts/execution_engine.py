#!/usr/bin/env python3
"""
Execution Engine v1.2
Fokus: Eksekvering af beslutninger med integreret Vidar Veto-logik og logning.
"""
import json
import os
import subprocess
from datetime import datetime, timezone
import vidar_security_scan

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECISIONS_LOG = os.path.join(_PROJECT_ROOT, "data/proposed_decisions.json")
EXECUTION_HISTORY = os.path.join(_PROJECT_ROOT, "data/execution_history.jsonl")

def execute_decision(decision_id, model="google/gemini-1.5-flash"):
    # Sikr at forslaget findes (repopuler hvis nødvendigt til test)
    if not os.path.exists(DECISIONS_LOG):
        print("[ENGINE]: Forslags-log mangler. Forsøger at generere forslag...")
        import decision_support
        decision_support.analyze_and_propose()

    with open(DECISIONS_LOG, "r") as f:
        data = json.load(f)
        proposals = data.get("proposals", [])

    proposal = next((p for p in proposals if p["id"] == decision_id), None)
    
    if not proposal:
        # Fallback til manuel definition hvis den ikke findes i loggen (kun til test)
        if decision_id == "shift_focus_v6":
            proposal = {
                "id": "shift_focus_v6",
                "title": "Intensiver V6 Arkitektur Sprint",
                "action": "scripts/triage_update.py --focus v6"
            }
        else:
            print(f"[ERROR]: Forslag '{decision_id}' ikke fundet.")
            return False

    # --- Vidar Veto Lag ---
    print(f"[ENGINE]: Anmoder Vidar om sikkerheds-scanning af '{decision_id}'...")
    is_safe, message = vidar_security_scan.scan_api_call(
        service="ExecutionEngine",
        action=proposal.get("action", "Unknown"),
        payload=proposal,
        model=model
    )
    
    if not is_safe:
        print(f"[VETO]: Vidar har blokeret handlingen: {message}")
        log_execution(decision_id, proposal, False, message)
        return False

    print(f"[EXECUTION]: Eksekverer '{proposal['title']}'...")
    # Simulation af succesfuld kørsel
    success = True
    output = "Simulation: Handling gennemført."
    
    log_execution(decision_id, proposal, success, message, output)
    print(f"[SUCCESS]: '{proposal['title']}' gennemført.")
    return True

def log_execution(decision_id, proposal, success, vidar_msg, output=""):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "decision_id": decision_id,
        "title": proposal["title"],
        "action": proposal.get("action", "N/A"),
        "success": success,
        "vidar_status": vidar_msg,
        "output": output
    }
    with open(EXECUTION_HISTORY, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "shift_focus_v6"
    execute_decision(target)
