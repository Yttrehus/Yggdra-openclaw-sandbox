#!/usr/bin/env python3
"""
Context-Aware Voice Summary v1.0
Fokus: Mundret opsummering af automatisk genererede kontekst-opgaver.
Del af V7.5 Kognitiv Proaktivitet.
"""
import json
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_FILE = os.path.join(_PROJECT_ROOT, "data/subtasks.json")

def get_context_tasks_vocalized():
    if not os.path.exists(TASKS_FILE):
        return ""
        
    with open(TASKS_FILE, "r") as f:
        all_tasks = json.load(f)
        
    context_tasks = all_tasks.get("context_guidance", [])
    pending_context = [t for t in context_tasks if t.get("status") == "pending"]
    
    if not pending_context:
        return ""
        
    count = len(pending_context)
    if count == 1:
        return f"Jeg har forberedt en opgave til dig baseret på din nuværende situation: {pending_context[0]['title']}. "
    else:
        return f"Jeg har automatisk oprettet {count} praktiske opgaver til dig pga. din dagsplan og rejsen i morgen. "

if __name__ == "__main__":
    print(get_context_tasks_vocalized())
