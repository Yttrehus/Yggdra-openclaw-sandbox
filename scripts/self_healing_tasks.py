#!/usr/bin/env python3
"""
Self-Healing Task Generator v1.0
Fokus: Automatisk generering af subtasks baseret på fejl i maintenance_report.md.
Del af V6.2 Handling & Eksekvering.
"""
import json
import os
import re
from datetime import datetime, timezone
import task_breakdown

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAINTENANCE_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")

def scan_for_issues():
    if not os.path.exists(MAINTENANCE_FILE):
        return []
    
    with open(MAINTENANCE_FILE, "r") as f:
        content = f.read()
    
    issues = []
    # Find linjer med [ERROR] eller [WARNING]
    for line in content.split('\n'):
        if "[ERROR]" in line or "[WARNING]" in line:
            issues.append(line.strip())
            
    return issues

def generate_healing_tasks():
    issues = scan_for_issues()
    if not issues:
        print("[SELF-HEALING]: Ingen kritiske fejl fundet i maintenance rapporten.")
        return
    
    print(f"[SELF-HEALING]: Fandt {len(issues)} potentielle problemer.")
    
    healing_tasks = []
    for issue in issues:
        # Simpel transformation fra fejl til opgave
        task_title = f"Fix: {issue.split(']', 1)[-1].strip()}"
        healing_tasks.append(task_title)
        
    # Tilføj disse til et 'system_health' mål
    task_breakdown.breakdown_goal("system_health", healing_tasks)
    print(f"[SELF-HEALING]: Genereret {len(healing_tasks)} healing tasks under 'system_health'.")

if __name__ == "__main__":
    generate_healing_tasks()
