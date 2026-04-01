#!/usr/bin/env python3
"""
Auto-Execution Engine v1.0
Fokus: Fuld autonom eksekvering af lav-risiko beslutninger.
Del af V7.4 Decision Auto-Execution.
"""
import json
import os
import execution_engine
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECISIONS_LOG = os.path.join(_PROJECT_ROOT, "data/proposed_decisions.json")

def auto_execute_low_risk():
    print("--- Auto-Execution: Tjekker for lav-risiko beslutninger ---")
    
    if not os.path.exists(DECISIONS_LOG):
        return
        
    with open(DECISIONS_LOG, "r") as f:
        data = json.load(f)
        proposals = data.get("proposals", [])
        
    for p in proposals:
        # Lav-risiko kriterier: f.eks. 'purge' handlinger eller monitorerings-skift
        if "purge" in p["id"] or "monitor" in p["id"]:
            print(f"[AUTO]: Detekteret lav-risiko handling: {p['title']}")
            success = execution_engine.execute_decision(p["id"])
            if success:
                print(f"[AUTO]: Succesfuldt eksekveret {p['id']} uden bruger-interaktion.")
                # Her kunne vi fjerne den fra proposals listen
        else:
            print(f"[MANUAL REQUIRED]: Handling {p['id']} kræver stadig bruger-accept.")

if __name__ == "__main__":
    auto_execute_low_risk()
