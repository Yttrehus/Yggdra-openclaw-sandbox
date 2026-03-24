#!/usr/bin/env python3
"""
YGGDRA VPS -> PC Sync Protocol (Draft)
Mål: Lukke kløften mellem instanser (Handling #7)
Fokus: Intelligence output, state-filer, logs.
"""

import os
import subprocess

VPS_IP = "72.62.61.51" # Fra context
REMOTE_PATH = "/root/Yggdra/"
LOCAL_PATH = "./"

TARGETS = [
    "scripts/ai_intelligence.py",
    "scripts/youtube_monitor.py",
    "data/intelligence_sources.json",
    "data/intelligence/",
]

def run_sync():
    print(f"--- Yggdra Sync: VPS -> PC ---")
    for target in TARGETS:
        remote = f"root@{VPS_IP}:{REMOTE_PATH}{target}"
        local = f"{LOCAL_PATH}{target}"
        print(f"Syncing: {target}...")
        # rsync logic skeleton
        # subprocess.run(["rsync", "-avz", remote, local])
    
    print("STATUS: Sync protocol designed. Awaiting execution permissions.")

if __name__ == "__main__":
    run_sync()
