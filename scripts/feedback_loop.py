#!/usr/bin/env python3
"""
Feedback Loop v1.0
Fokus: Indsamling og lagring af brugerens svar på Goal Drills.
Del af V6.1 Hukommelses-evolution.
"""
import json
import os
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODES_FILE = os.path.join(_PROJECT_ROOT, "data/episodes.jsonl")
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")

def log_drill_feedback(goal_id, feedback_text):
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    
    # 1. Log til episoder (Narrativ kontinuitet)
    episode = {
        "timestamp": timestamp,
        "event": "goal_drill_feedback",
        "goal_id": goal_id,
        "feedback": feedback_text,
        "type": "user_interaction"
    }
    with open(EPISODES_FILE, "a") as f:
        f.write(json.dumps(episode) + "\n")
    
    # 2. Opdater målets historie (Strategisk fokus)
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            goals = json.load(f)
        
        for goal in goals:
            if goal["id"] == goal_id:
                goal["last_updated"] = timestamp
                goal["history"].append({
                    "timestamp": timestamp,
                    "delta": 0,
                    "comment": f"Feedback modtaget: {feedback_text}"
                })
                break
        
        with open(GOALS_FILE, "w") as f:
            json.dump(goals, f, indent=2)
            
    print(f"[FEEDBACK LOOP]: Feedback gemt for '{goal_id}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        log_drill_feedback(sys.argv[1], " ".join(sys.argv[2:]))
    else:
        print("Usage: feedback_loop.py <goal_id> <feedback_text>")
