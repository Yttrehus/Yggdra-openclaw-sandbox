#!/usr/bin/env python3
"""
Pipeline Watchdog v1.0
Fokus: Autonom genstart af fejlede jobs og selv-healing.
Inspireret af "Self-healing crontab patterns".
"""

import os
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Config
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
INTELLIGENCE_DIR = os.path.join(_PROJECT_ROOT, "data/intelligence")

# Jobs der skal overvåges og evt. genstartes
CRITICAL_JOBS = {
    "daily_sweep": {
        "script": "scripts/daily_sweep.py", # Dette script findes på VPS
        "expected_output": "data/intelligence/daily_{date}.md",
        "max_age_hours": 28
    },
    "fact_extraction": {
        "script": "SIP.agent-sandbox/fact_extraction_v2/subagent_orchestrator.py",
        "expected_output": "data/extracted_facts.json",
        "max_age_hours": 48
    }
}

def check_and_heal():
    print(f"--- Pipeline Watchdog Run: {datetime.now(timezone.utc).isoformat()} ---")
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    for name, cfg in CRITICAL_JOBS.items():
        pattern = cfg["expected_output"]
        if "{date}" in pattern:
            path = Path(_PROJECT_ROOT) / pattern.format(date=today_str)
            if not path.exists():
                path = Path(_PROJECT_ROOT) / pattern.format(date=yesterday_str)
        else:
            path = Path(_PROJECT_ROOT) / pattern
            
        should_restart = False
        if not path.exists():
            print(f"[WATCHDOG] {name} output MISSING. Triggering restart...")
            should_restart = True
        else:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            age_hours = (now - mtime).total_seconds() / 3600
            if age_hours > cfg["max_age_hours"]:
                print(f"[WATCHDOG] {name} is STALE ({age_hours:.1f}h). Triggering restart...")
                should_restart = True
        
        if should_restart:
            script_path = Path(_PROJECT_ROOT) / cfg["script"]
            if script_path.exists():
                print(f"[WATCHDOG] Executing restart: {cfg['script']}")
                # I sandboxen simulerer vi kun genstart
                # subprocess.run(["python3", str(script_path)], check=True)
                print(f"[WATCHDOG] Simulation mode: Restart command would be issued here.")
            else:
                print(f"[WATCHDOG] ERROR: {cfg['script']} NOT FOUND. Cannot heal.")

if __name__ == "__main__":
    check_and_heal()
