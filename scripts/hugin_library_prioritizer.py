#!/usr/bin/env python3
"""
Hugin Library Prioritizer v1.0
Fokus: Strategisk prioritering af biblioteks-integrationer baseret på Ratatosks plan.
Del af V8 Collaborative Intelligence / V7.1 Execution.
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_FILE = os.path.join(_PROJECT_ROOT, "LIB.research/V7_integration_plan.json")

def prioritize_libraries():
    print("--- Hugin: Prioriterer biblioteks-integrationer for V7.1 ---")
    
    if not os.path.exists(PLAN_FILE):
        print("[ERROR]: Integrations-plan ikke fundet. Kør ratatosk_v7_plan.py først.")
        return
        
    with open(PLAN_FILE, "r") as f:
        plan = json.load(f)
        
    # Strategisk analyse af rækkefølge
    # Vi prioriterer Google Workspace først pga. kalender-afhængighed for TTL og Agenda.
    # Derefter Notion pga. central projektstyring.
    # Sidst ElevenLabs da det er et forbedrings-lag (SSML).
    
    order = ["google_workspace", "notion", "elevenlabs"]
    
    prioritized_list = []
    for key in order:
        if key in plan:
            prioritized_list.append({
                "target": key,
                "libraries": plan[key]["libraries"],
                "reason": f"Kritisk for {key} integration."
            })
            
    print("[Hugin]: Strategisk rækkefølge fastlagt:")
    for i, item in enumerate(prioritized_list, 1):
        print(f"  {i}. {item['target']} ({', '.join(item['libraries'])})")
        
    return prioritized_list

if __name__ == "__main__":
    prioritize_libraries()
