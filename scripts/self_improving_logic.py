#!/usr/bin/env python3
"""
Self-Improving Logic v1.0
Fokus: Agenter der lærer af Vidars vetoer og optimerer fremtidige planer.
Del af V8 Collaborative Intelligence.
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXECUTION_HISTORY = os.path.join(_PROJECT_ROOT, "data/execution_history.jsonl")
LEARNINGS_FILE = os.path.join(_PROJECT_ROOT, "data/LEARNINGS.md")

def analyze_vetoes_and_learn():
    print("--- Self-Improving Logic: Analyserer Vidar Vetoer ---")
    
    if not os.path.exists(EXECUTION_HISTORY):
        return
    
    vetoes = []
    with open(EXECUTION_HISTORY, "r") as f:
        for line in f:
            entry = json.loads(line)
            if not entry.get("success") and "VETO" in entry.get("vidar_status", ""):
                vetoes.append(entry)
                
    if not vetoes:
        print("[LEARNING]: Ingen nye vetoer at lære fra.")
        return

    print(f"[LEARNING]: Fandt {len(vetoes)} vetoer. Udleder forbedringer...")
    
    new_learnings = []
    for v in vetoes:
        learning = f"- [V8 LEARNING] Handling '{v['title']}' blev blokeret pga: {v['vidar_status']}. Fremtidige planer skal inkludere eksplicit sikkerheds-clearing for denne type operationer. (Logget: {datetime.now().strftime('%Y-%m-%d')})"
        new_learnings.append(learning)

    # Gem læringer
    with open(LEARNINGS_FILE, "a") as f:
        f.write("\n" + "\n".join(new_learnings) + "\n")
        
    print(f"[SUCCESS]: Tilføjet {len(new_learnings)} nye læringer til data/LEARNINGS.md.")

if __name__ == "__main__":
    analyze_vetoes_and_learn()
