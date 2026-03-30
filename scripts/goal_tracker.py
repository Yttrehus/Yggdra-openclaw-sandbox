#!/usr/bin/env python3
"""
Long-term Goal Tracker v1.0
Fokus: Tracking af strategiske mål og deres fremdrift over tid.
Del af V6.1 Hukommelses-evolution.
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")

def load_goals():
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        return json.load(f)

def save_goals(goals):
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=2)

def update_goal_progress(goal_id, progress_delta, comment=""):
    goals = load_goals()
    for goal in goals:
        if goal["id"] == goal_id:
            goal["progress"] = min(100, goal["progress"] + progress_delta)
            goal["last_updated"] = datetime.utcnow().isoformat() + "Z"
            goal["history"].append({
                "timestamp": goal["last_updated"],
                "delta": progress_delta,
                "comment": comment
            })
            break
    save_goals(goals)
    print(f"[GOAL TRACKER]: Opdateret mål '{goal_id}' til {goal['progress']}% progress.")

if __name__ == "__main__":
    # Initialiser standard mål hvis filen ikke findes
    if not os.path.exists(GOALS_FILE):
        initial_goals = [
            {
                "id": "v6_completion",
                "title": "Yggdra V6 Integration",
                "progress": 85,
                "category": "Architecture",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "history": []
            },
            {
                "id": "notion_init",
                "title": "Notion Live Initialization",
                "progress": 40,
                "category": "Infrastructure",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "history": []
            }
        ]
        save_goals(initial_goals)
        print("[GOAL TRACKER]: Initialiseret standard mål.")
    
    # Eksempel på opdatering
    update_goal_progress("v6_completion", 2, "Implementeret Goal Tracker PoC")
