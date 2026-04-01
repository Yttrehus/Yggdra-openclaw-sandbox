#!/usr/bin/env python3
"""
Auto-Execution Feedback v1.0
Fokus: Generering af mundret feedback til voice-interfacet om autonome handlinger.
Del af V7.4 Decision Auto-Execution.
"""
import json
import os
from datetime import datetime, timedelta, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXECUTION_HISTORY = os.path.join(_PROJECT_ROOT, "data/execution_history.jsonl")

def get_recent_auto_actions():
    if not os.path.exists(EXECUTION_HISTORY):
        return ""
    
    recent_actions = []
    now = datetime.now(timezone.utc)
    
    with open(EXECUTION_HISTORY, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                # Vi kigger kun på handlinger fra de sidste 24 timer
                if now - ts < timedelta(hours=24):
                    # Her simulerer vi et tjek for om det var 'auto' (id indeholder purge i denne demo)
                    if "purge" in entry.get("decision_id", ""):
                        recent_actions.append(entry['title'])
            except:
                continue
                
    if not recent_actions:
        return ""
        
    if len(recent_actions) == 1:
        return f"Mens du var væk, har jeg automatisk gennemført: {recent_actions[0]}. "
    else:
        return f"Jeg har i baggrunden optimeret systemet ved at gennemføre {len(recent_actions)} vedligeholdelses-opgaver. "

if __name__ == "__main__":
    print(get_recent_auto_actions())
