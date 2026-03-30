#!/usr/bin/env python3
"""
Task Breakdown v1.0
Fokus: Nedbrydning af strategiske mål til konkrete, eksekverbare opgaver.
Del af V6.2 Handling & Eksekvering.
"""
import json
import os
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")
TASKS_FILE = os.path.join(_PROJECT_ROOT, "data/subtasks.json")

def breakdown_goal(goal_id, subtasks_list):
    """Nedbryder et specifikt mål til en liste af subtasks."""
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    
    if not os.path.exists(TASKS_FILE):
        all_tasks = {}
    else:
        with open(TASKS_FILE, "r") as f:
            all_tasks = json.load(f)
            
    tasks = []
    for i, task_title in enumerate(subtasks_list):
        tasks.append({
            "id": f"{goal_id}_task_{i+1}",
            "title": task_title,
            "status": "pending",
            "created_at": timestamp
        })
        
    all_tasks[goal_id] = tasks
    
    with open(TASKS_FILE, "w") as f:
        json.dump(all_tasks, f, indent=2)
        
    print(f"[TASK BREAKDOWN]: Mål '{goal_id}' nedbrudt til {len(tasks)} opgaver.")

if __name__ == "__main__":
    # Eksempel: Nedbrydning af Notion Integration
    notion_tasks = [
        "Opsæt NOTION_API_KEY i miljøet",
        "Kør db_init_v2.py for at oprette databaser",
        "Verificer synkronisering med notion_sync.py",
        "Valider dashboard visning på mobil"
    ]
    breakdown_goal("notion_init", notion_tasks)
