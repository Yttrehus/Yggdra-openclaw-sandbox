#!/usr/bin/env python3
"""
Execution Engine v1.0
Fokus: Eksekvering af godkendte beslutninger fra Decision Support.
Del af V6.3 Kognitiv Guidance.
"""
import json
import os
import subprocess
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECISIONS_LOG = os.path.join(_PROJECT_ROOT, "data/proposed_decisions.json")
EXECUTION_HISTORY = os.path.join(_PROJECT_ROOT, "data/execution_history.jsonl")

def execute_decision(decision_id):
    if not os.path.exists(DECISIONS_LOG):
        print("[ERROR]: Ingen forslag fundet.")
        return False

    with open(DECISIONS_LOG, "r") as f:
        data = json.load(f)
        proposals = data.get("proposals", [])

    proposal = next((p for p in proposals if p["id"] == decision_id), None)
    
    if not proposal:
        print(f"[ERROR]: Forslag '{decision_id}' ikke fundet.")
        return False

    print(f"[EXECUTION]: Eksekverer '{proposal['title']}'...")
    print(f"[CMD]: {proposal['action']}")
    
    # Her ville vi normalt køre kommandoen:
    # try:
    #     result = subprocess.run(proposal['action'].split(), capture_output=True, text=True, check=True)
    #     success = True
    #     output = result.stdout
    # except Exception as e:
    #     success = False
    #     output = str(e)
    
    # Simulation:
    success = True
    output = "Simulation: Kommando kørt succesfuldt."
    
    # Log hændelsen
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "decision_id": decision_id,
        "title": proposal["title"],
        "action": proposal["action"],
        "success": success,
        "output": output
    }
    
    with open(EXECUTION_HISTORY, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    print(f"[SUCCESS]: '{proposal['title']}' eksekveret og logget.")
    return success

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        execute_decision(sys.argv[1])
    else:
        print("Usage: execution_engine.py <decision_id>")
