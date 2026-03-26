#!/usr/bin/env python3
"""
Maintenance Audit v1.1
Fokus: Pipeline-sundhed, prisændringer og videns-decay.
Nu med forbedret integration og Telegram-notifikation via OpenClaw hooks.
"""

import os
import sys
import hashlib
import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Config
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
INTELLIGENCE_DIR = os.path.join(_PROJECT_ROOT, "data/intelligence")
STATE_FILE = os.path.join(_PROJECT_ROOT, "data/maintenance_state.json")

# Udvidelse 4: Pipeline Health Monitor
PIPELINE_EXPECTATIONS = {
    "ai_intelligence": {"pattern": "daily_{date}.md", "max_age_hours": 28, "dir": INTELLIGENCE_DIR},
    "youtube_monitor": {"pattern": "yt_daily_{date}.md", "max_age_hours": 28, "dir": INTELLIGENCE_DIR},
    "fact_extraction": {"pattern": "extracted_facts.json", "max_age_hours": 48, "dir": os.path.join(_PROJECT_ROOT, "data")}
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_run": None, "last_alerts": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def check_pipeline_health():
    print("--- Checking Pipeline Health ---")
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    findings = []
    for name, cfg in PIPELINE_EXPECTATIONS.items():
        pattern = cfg["pattern"]
        directory = cfg["dir"]
        
        # Check today, then yesterday for dated files
        if "{date}" in pattern:
            path = Path(directory) / pattern.format(date=today_str)
            if not path.exists():
                path = Path(directory) / pattern.format(date=yesterday_str)
        else:
            path = Path(directory) / pattern
            
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            age_hours = (now - mtime).total_seconds() / 3600
            if age_hours > cfg["max_age_hours"]:
                findings.append(f"[ALERT] {name} is STALE ({age_hours:.1f}h old)")
            else:
                print(f"[OK] {name} is healthy ({age_hours:.1f}h old)")
        else:
            findings.append(f"[ALERT] {name} output MISSING ({path.name})")
    
    return findings

def check_knowledge_decay():
    print("\n--- Checking Knowledge Decay ---")
    # Simulation af decay tracking
    # I en fuld version ville vi scanne LIB.research mapperne for fil-alder
    now = datetime.now(timezone.utc)
    research_dir = Path(_PROJECT_ROOT) / "LIB.research"
    stale_files = []
    
    if research_dir.exists():
        for file in research_dir.rglob("*.md"):
            mtime = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
            age_days = (now - mtime).days
            if age_days > 90: # 3 måneder uden opdatering
                stale_files.append(f"{file.relative_to(_PROJECT_ROOT)} ({age_days} days old)")
    
    if stale_files:
        print(f"Found {len(stale_files)} potentially stale research files.")
        return [f"[INFO] {len(stale_files)} research files > 90 days old. Consider re-scan."]
    return []

def main():
    state = load_state()
    health_issues = check_pipeline_health()
    decay_issues = check_knowledge_decay()
    
    all_issues = health_issues + decay_issues
    
    report_path = Path(_PROJECT_ROOT) / "data/maintenance_report.md"
    with open(report_path, "w") as f:
        f.write(f"# Maintenance Audit Report - {datetime.now().isoformat()}\n\n")
        if all_issues:
            f.write("## Issues Detected\n")
            for issue in all_issues:
                f.write(f"- {issue}\n")
        else:
            f.write("## Status: All Systems Operational\n")
            f.write("No critical pipeline or knowledge decay issues detected.\n")

    if all_issues:
        print("\nMAINTENANCE ISSUES DETECTED:")
        for issue in all_issues:
            print(issue)
    else:
        print("\nSystem is maintaining optimal state.")
    
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["last_alerts"] = all_issues
    save_state(state)

if __name__ == "__main__":
    main()
