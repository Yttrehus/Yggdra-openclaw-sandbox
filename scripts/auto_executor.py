#!/usr/bin/env python3
"""
Auto-Executor v1.0
Fokus: Autonom eksekvering af lav-risiko beslutninger.
Del af V7.4 Decision Auto-Execution.
"""
import json
import os
import subprocess
from datetime import datetime, timezone
import execution_engine
import decision_support

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTO_EXEC_LOG = os.path.join(_PROJECT_ROOT, "data/auto_execution_history.jsonl")

def run_auto_execution():
    print("--- Auto-Executor: Scanner for lav-risiko forslag ---")
    
    # 1. Generer forslag
    proposals = decision_support.analyze_and_propose()
    
    if not proposals:
        print("[AUTO]: Ingen forslag fundet.")
        return

    # 2. Identificer og eksekver lav-risiko forslag
    for p in proposals:
        if p.get("risk_level") == "low":
            print(f"[AUTO]: Detekteret lav-risiko forslag: '{p['title']}'.")
            print(f"[AUTO]: Eksekverer autonomt...")
            
            success = execution_engine.execute_decision(p["id"])
            
            if success:
                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                    "decision_id": p["id"],
                    "title": p["title"],
                    "status": "auto_executed"
                }
                with open(AUTO_EXEC_LOG, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
                print(f"[SUCCESS]: '{p['title']}' gennemført autonomt.")
            else:
                print(f"[ERROR]: Kunne ikke eksekvere '{p['title']}'.")
        else:
            print(f"[INFO]: Forslag '{p['title']}' kræver manuel godkendelse (Risk: {p.get('risk_level')}).")

if __name__ == "__main__":
    run_auto_execution()
