#!/usr/bin/env python3
"""
Task Completion v1.0
Fokus: Markering af opgaver som færdige og automatisk opdatering af mål-progress.
Del af V6.2 Handling & Eksekvering.
"""
import json
import os
from datetime import datetime, timezone
import goal_tracker

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_FILE = os.path.join(_PROJECT_ROOT, "data/subtasks.json")
GOALS_FILE = os.path.join(_PROJECT_ROOT, "data/long_term_goals.json")

def complete_task(goal_id, task_id, comment=""):
    """Marker en task som færdig og opdater det overordnede mål."""
    if not os.path.exists(TASKS_FILE):
        print(f"[ERROR]: {TASKS_FILE} ikke fundet.")
        return

    with open(TASKS_FILE, "r") as f:
        all_tasks = json.load(f)

    if goal_id not in all_tasks:
        print(f"[ERROR]: Mål '{goal_id}' ikke fundet i subtasks.")
        return

    found = False
    goal_tasks = all_tasks[goal_id]
    for task in goal_tasks:
        if task["id"] == task_id:
            if task["status"] == "completed":
                print(f"[INFO]: Task '{task_id}' er allerede markeret som færdig.")
                return
            task["status"] = "completed"
            task["completed_at"] = datetime.now(timezone.utc).isoformat() + "Z"
            found = True
            break

    if not found:
        print(f"[ERROR]: Task '{task_id}' ikke fundet under mål '{goal_id}'.")
        return

    # Gem opdaterede tasks
    with open(TASKS_FILE, "w") as f:
        json.dump(all_tasks, f, indent=2)

    # Beregn ny progress for målet
    completed_count = sum(1 for t in goal_tasks if t["status"] == "completed")
    total_count = len(goal_tasks)
    
    # Simpel progress: Vi antager at subtasks udgør en del af målet.
    # Her lader vi hver subtask tælle for en procentdel af den manglende progress?
    # Eller vi sætter målets progress direkte baseret på subtask ratio hvis det er relevant.
    # For denne PoC: Vi øger progress med en fast delta pr. task.
    progress_per_task = 100 // total_count if total_count > 0 else 0
    
    print(f"[TASK COMPLETION]: Task '{task_id}' markeret som færdig.")
    
    # Opdater det overordnede mål via goal_tracker
    goal_tracker.update_goal_progress(goal_id, progress_per_task, f"Færdiggjort opgave: {task_id}. {comment}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        g_id = sys.argv[1]
        t_id = sys.argv[2]
        msg = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        complete_task(g_id, t_id, msg)
    else:
        print("Usage: task_completion.py <goal_id> <task_id> [comment]")
