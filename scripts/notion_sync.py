import os
import sys
import argparse
import re
from datetime import datetime

def extract_status_from_context():
    """Ekstraherer aktive projekter og status fra CONTEXT.md"""
    projects = []
    context_path = "CONTEXT.md"
    if not os.path.exists(context_path):
        return projects

    with open(context_path, "r") as f:
        content = f.read()

    # Find sektionen 'Aktive projekter'
    active_section = re.search(r"### Aktive projekter\n(.*?)(?:\n\n|\n##|$)", content, re.DOTALL)
    if active_section:
        lines = active_section.group(1).strip().split("\n")
        for line in lines:
            match = re.search(r"- \*\*([\w\.]+):\*\* (.*)", line)
            if match:
                projects.append({
                    "name": match.group(1),
                    "status": match.group(2),
                    "last_updated": datetime.now().strftime("%Y-%m-%d")
                })
    return projects

def sync_to_notion():
    """
    Syncs current project status from CONTEXT.md to Notion.
    Placeholder script until MCP/API access is fully established.
    """
    print("--- Notion Sync Engine (v0.1) ---")
    projects = extract_status_from_context()
    
    if not projects:
        print("No active projects found in CONTEXT.md.")
        return

    print(f"Found {len(projects)} projects to sync:")
    for p in projects:
        print(f"  > {p['name']}: {p['status']}")

    print("\nNOTION_API_STATUS: Awaiting key integration.")
    print("READY_TO_PUSH: True")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-end", action="store_true")
    args = parser.parse_args()
    
    if args.session_end:
        sync_to_notion()
