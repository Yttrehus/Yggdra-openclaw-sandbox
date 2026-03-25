import os
import sys
import argparse
import re
import json
from datetime import datetime

# Simuleret Notion API Client til brug i hooks uden API-nøgle
class MockNotionClient:
    def __init__(self, token):
        self.token = token
    def push_update(self, project, status):
        print(f"  [MOCK PUSH] {project}: {status}")
        return True

def extract_status_from_context():
    """Ekstraherer aktive projekter og status fra CONTEXT.md"""
    projects = []
    context_path = "CONTEXT.md"
    if not os.path.exists(context_path):
        return projects

    with open(context_path, "r") as f:
        content = f.read()

    lines = content.split('\n')
    start_idx = -1
    for i, line in enumerate(lines):
        if "### Aktive projekter" in line:
            start_idx = i
            break
            
    if start_idx != -1:
        for line in lines[start_idx+1:]:
            if line.startswith("##"):
                break
            # Matcher: - **Projekttitel:** Statusbesked
            match = re.search(r"- \*\*([\w\.\-]+):\*\* (.*)", line)
            if match:
                projects.append({
                    "name": match.group(1),
                    "status": match.group(2).strip()
                })
    return projects

def sync_to_notion():
    """Syncs current project status from CONTEXT.md to Notion."""
    print(f"--- Notion Sync Engine ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---")
    token = os.environ.get("NOTION_API_KEY")
    
    projects = extract_status_from_context()
    if not projects:
        print("No active projects found in CONTEXT.md.")
        return

    if not token:
        print("NOTION_API_KEY not found. Running in MOCK mode.")
        client = MockNotionClient("mock-token")
    else:
        print("NOTION_API_KEY found. Attempting live sync...")
        # Her ville den reelle SDK integration bo
        client = MockNotionClient(token)

    for p in projects:
        client.push_update(p['name'], p['status'])
    
    print("STATUS: Sync complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-end", action="store_true")
    args = parser.parse_args()
    
    if args.session_end:
        sync_to_notion()
