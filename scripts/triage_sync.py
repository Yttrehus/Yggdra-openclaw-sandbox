#!/usr/bin/env python3
"""
Triage Sync v1.0
Fokus: Brobygning mellem TRIAGE.md (Taktisk) og Goal Tracker (Strategisk).
Del af V6.1 Hukommelses-evolution.
"""
import os
import re
import goal_tracker

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAGE_FILE = os.path.join(_PROJECT_ROOT, "0_backlog/TRIAGE.md")

def analyze_triage_completion():
    if not os.path.exists(TRIAGE_FILE):
        return 0, 0
    
    with open(TRIAGE_FILE, "r") as f:
        content = f.read()
    
    # Find rækker i tabeller der indeholder 'DEPLOYED', 'OK', eller 'Gennemført'
    completed_patterns = [r'DEPLOYED', r'OK', r'Gennemført']
    
    total_items = 0
    completed_items = 0
    
    # Enkel tabel-række parsing
    lines = content.split('\n')
    for line in lines:
        if '|' in line and not line.strip().startswith('|---'):
            # Ignorer header-lignende rækker (mere end 2 pipes typisk)
            if line.count('|') >= 3:
                total_items += 1
                if any(re.search(p, line) for p in completed_patterns):
                    completed_items += 1
    
    return completed_items, total_items

def sync_to_goals():
    comp, total = analyze_triage_completion()
    if total == 0:
        return
    
    # Beregn en vægtet fremdrift (simpelt for nu)
    # Vi mapper TRIAGE overordnet til 'v6_completion' i denne PoC
    progress = int((comp / total) * 100)
    
    print(f"[TRIAGE SYNC]: Analyse færdig. {comp}/{total} opgaver gennemført ({progress}%).")
    
    # Opdater strategisk mål (v6_completion)
    # Vi henter nuværende for at se om vi skal lave en delta
    goals = goal_tracker.load_goals()
    current_progress = 0
    for g in goals:
        if g['id'] == 'v6_completion':
            current_progress = g['progress']
            break
    
    delta = progress - current_progress
    if delta != 0:
        goal_tracker.update_goal_progress("v6_completion", delta, f"Auto-sync fra TRIAGE.md ({comp}/{total})")
    else:
        print("[TRIAGE SYNC]: Ingen ændring i progress.")

if __name__ == "__main__":
    sync_to_goals()
