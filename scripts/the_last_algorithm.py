#!/usr/bin/env python3
"""
The Last Algorithm (v1.0)
Arkitektur:
1. Load Current State (CONTEXT.md)
2. Load Ideal State (BLUEPRINT.md + MISSION.md)
3. Generate Gap Analysis via LLM
4. Output Actionable TODOs
"""

import os
import sys
import re
from openai import OpenAI

# Config
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

def _load_openai_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key: return key
    creds_path = os.path.join(_PROJECT_ROOT, "data", "CREDENTIALS.md")
    try:
        with open(creds_path, 'r') as f:
            return f.read().split('`')[1]
    except: return None

def run_analysis():
    print("--- The Last Algorithm: Gap Analysis ---")
    
    key = _load_openai_key()
    if not key:
        print("Error: OpenAI API Key not found. Analysis aborted.")
        return

    client = OpenAI(api_key=key)
    
    # Files to read
    files = {
        "current": "CONTEXT.md",
        "ideal": "BLUEPRINT.md",
        "mission": "MISSION.md"
    }
    
    content = {}
    for name, path in files.items():
        try:
            with open(os.path.join(_PROJECT_ROOT, path), 'r') as f:
                content[name] = f.read()
        except FileNotFoundError:
            content[name] = f"[File {path} not found]"

    prompt = f"""
Du er Yggdras strategiske motor (The Last Algorithm).
Din opgave er at sammenligne projektets aktuelle status med den overordnede vision og identificere kritiske huller.

--- IDEAL STATE (BLUEPRINT) ---
{content['ideal']}

--- MISSION ---
{content['mission']}

--- CURRENT STATE (CONTEXT) ---
{content['current']}

--- OPGAVE ---
Identificér de 3 vigtigste 'Gaps' mellem nuværende status og ideal-tilstand.
For hvert gap, giv en konkret handling (TODO) der kan udføres i næste session.
Formatér svaret i Markdown.
"""

    try:
        print("Analyzing project trajectory...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        analysis = response.choices[0].message.content
        print("\n--- ANALYSIS RESULTS ---")
        print(analysis)
        
        # Save to file
        with open(os.path.join(_PROJECT_ROOT, "data/gap_analysis_latest.md"), 'w') as f:
            f.write(analysis)
        print(f"\nAnalysis saved to data/gap_analysis_latest.md")
        
    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    run_analysis()
