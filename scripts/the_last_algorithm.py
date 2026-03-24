#!/usr/bin/env python3
"""
The Last Algorithm (PAI Principal)
1. Observér CURRENT STATE (CONTEXT.md / NOW.md)
2. Sammenlign med IDEAL STATE (MISSION.md / BLUEPRINT.md)
3. Identificér Gaps og foreslå handlinger
"""

import os
import sys

def run_gap_analysis():
    print("--- The Last Algorithm: Gap Analysis ---")
    
    # 1. Load context
    # In a real run, this would use LLM to compare files.
    # Here we implement the logic skeleton.
    
    paths = {
        "current": "CONTEXT.md",
        "ideal": "BLUEPRINT.md",
        "mission": "MISSION.md"
    }
    
    for name, path in paths.items():
        if not os.path.exists(path):
            print(f"Warning: {path} missing.")
            
    print("STATUS: Logic skeleton active. Awaiting LLM integration for deep comparison.")

if __name__ == "__main__":
    run_gap_analysis()
