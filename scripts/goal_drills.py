#!/usr/bin/env python3
"""
Goal Drills v1.0
Fokus: Proaktive spørgsmål og dybdeborende analyse af mål med lav fremdrift.
Del af V6.1 Hukommelses-evolution.
"""
import json
import os
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")

def get_stagnant_goals(threshold_days=3):
    if not os.path.exists(GOALS_FILE):
        return []
    
    with open(GOALS_FILE, "r") as f:
        goals = json.load(f)
    
    stagnant = []
    now = datetime.now(timezone.utc)
    
    for goal in goals:
        ts = goal["last_updated"].replace('Z', '')
        if '+' in ts:
            ts = ts.split('+')[0]
        last_updated = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        days_since = (now - last_updated).days
        
        if days_since >= threshold_days and goal["progress"] < 100:
            stagnant.append({
                "title": goal["title"],
                "days": days_since,
                "progress": goal["progress"]
            })
    
    return stagnant

def generate_drill_prompts():
    stagnant = get_stagnant_goals()
    if not stagnant:
        return None
    
    prompts = []
    for goal in stagnant:
        prompts.append(f"Jeg bemærker, at '{goal['title']}' har stået stille på {goal['progress']}% i {goal['days']} dage. Er der noget, der blokerer os her?")
    
    return prompts

if __name__ == "__main__":
    drills = generate_drill_prompts()
    if drills:
        for d in drills:
            print(f"[GOAL DRILL]: {d}")
        
        # Gem til voice simulator
        with open(os.path.join(_PROJECT_ROOT, "data/goal_drills.json"), "w") as f:
            json.dump({"drills": drills, "timestamp": datetime.now(timezone.utc).isoformat()}, f)
    else:
        print("Ingen stagnante mål fundet.")
        if os.path.exists(os.path.join(_PROJECT_ROOT, "data/goal_drills.json")):
            os.remove(os.path.join(_PROJECT_ROOT, "data/goal_drills.json"))
