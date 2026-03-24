#!/usr/bin/env python3
"""
YGGDRA VPS -> PC Sync Protocol (v1.0)
Mål: Lukke kløften mellem instanser (Handling #7)
Metode: Rsync-baseret synkronisering af intelligence data og scripts.
"""

import os
import subprocess
import argparse

VPS_IP = "72.62.61.51"
REMOTE_USER = "root"
REMOTE_ROOT = "/root/Yggdra/"
LOCAL_ROOT = "./"

# Definer stier der skal synkroniseres (relativt til root)
SYNC_TARGETS = [
    {"path": "scripts/ai_intelligence.py", "type": "file"},
    {"path": "scripts/youtube_monitor.py", "type": "file"},
    {"path": "data/intelligence_sources.json", "type": "file"},
    {"path": "data/intelligence/", "type": "dir"},
]

def run_rsync(target, dry_run=False):
    remote_path = f"{REMOTE_USER}@{VPS_IP}:{REMOTE_ROOT}{target['path']}"
    local_path = os.path.join(LOCAL_ROOT, target['path'])
    
    # Sørg for at lokale mapper eksisterer
    if target['type'] == 'dir':
        os.makedirs(local_path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

    cmd = ["rsync", "-avz"]
    if dry_run:
        cmd.append("--dry-run")
    
    cmd.extend([remote_path, local_path])
    
    print(f"Executing: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Failed to execute rsync: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sync Yggdra assets from VPS to PC")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be synced without making changes")
    parser.add_argument("--target", help="Specific target path to sync (optional)")
    args = parser.parse_args()

    print(f"--- Yggdra Sync Tool ---")
    
    for target in SYNC_TARGETS:
        if args.target and args.target not in target['path']:
            continue
        run_rsync(target, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
