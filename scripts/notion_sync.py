import os
import sys
import argparse
from datetime import datetime

def sync_to_notion():
    """
    Syncs current project status from CONTEXT.md to Notion.
    Placeholder script until MCP/API access is fully established in the hook context.
    """
    print("--- Notion Sync (Draft) ---")
    context_path = "CONTEXT.md"
    if not os.path.exists(context_path):
        print(f"Error: {context_path} not found.")
        return

    # Mock logic: Extract current status and targets
    print(f"Reading {context_path}...")
    # I en rigtig implementation ville vi bruge Notion SDK her.
    print("NOTION_SYNC_RESULT: SKIPPED (Waiting for API Key integration)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-end", action="store_true")
    args = parser.parse_args()
    
    if args.session_end:
        sync_to_notion()
