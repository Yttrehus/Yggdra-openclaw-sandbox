#!/usr/bin/env python3
"""
Voice Confirmation v1.0
Fokus: Generering af verbale bekræftelser på udførte handlinger.
Del af V6.3 Kognitiv Guidance.
"""
import json
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXECUTION_HISTORY = os.path.join(_PROJECT_ROOT, "data/execution_history.jsonl")

def get_last_confirmation():
    if not os.path.exists(EXECUTION_HISTORY):
        return ""

    with open(EXECUTION_HISTORY, "r") as f:
        lines = f.readlines()
        if not lines:
            return ""
        
        last_entry = json.loads(lines[-1])
        if last_entry.get("success"):
            return f"Jeg har nu gennemført handlingen: {last_entry['title']}, som vi aftalte. "
        else:
            return f"Der opstod desværre en fejl under udførelsen af: {last_entry['title']}. "

if __name__ == "__main__":
    print(get_last_confirmation())
