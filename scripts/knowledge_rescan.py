#!/usr/bin/env python3
"""
Knowledge Rescan Tool v1.0
Identificerer forældede research-filer og forbereder prompts til opdatering.
Baseret på 90-dages decay reglen fra maintenance_audit.py.
"""
import os
from pathlib import Path
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = Path(_PROJECT_ROOT) / "LIB.research"

def find_stale_files(days=90):
    now = datetime.now(timezone.utc)
    stale = []
    for file in RESEARCH_DIR.rglob("*.md"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
        age_days = (now - mtime).days
        if age_days >= days:
            stale.append((file, age_days))
    return sorted(stale, key=lambda x: x[1], reverse=True)

def main():
    print(f"--- Knowledge Rescan Audit ---")
    stale_files = find_stale_files()
    if not stale_files:
        print("Ingen forældede filer fundet.")
        return

    print(f"Fundet {len(stale_files)} filer ældre end 90 dage:\n")
    
    rescan_list = Path(_PROJECT_ROOT) / "0_backlog/RESCAN_LIST.md"
    with open(rescan_list, "w") as f:
        f.write("# Knowledge Rescan List\n\n")
        f.write("Filer der kræver opdatering pga. epistemisk decay (>90 dage).\n\n")
        f.write("| Fil | Alder (dage) | Status |\n")
        f.write("| :--- | :--- | :--- |\n")
        for path, age in stale_files:
            rel_path = path.relative_to(_PROJECT_ROOT)
            print(f"- {rel_path} ({age} dage)")
            f.write(f"| `{rel_path}` | {age} | [ ] Planlagt |\n")
            
    print(f"\nListe gemt i {rescan_list.relative_to(_PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
