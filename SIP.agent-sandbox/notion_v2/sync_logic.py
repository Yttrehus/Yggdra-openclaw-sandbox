import os
import requests
import json
from datetime import datetime

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

def add_project_to_notion(name, status, stage, next_step):
    if not NOTION_TOKEN or not DATABASE_ID:
        print("Error: Notion credentials missing.")
        return

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Navn": {"title": [{"text": {"content": name}}]},
            "Status": {"select": {"name": status}},
            "Stage": {"select": {"name": stage}},
            "Næste Step": {"rich_text": [{"text": {"content": next_step}}]},
            "Sidst Opdateret": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"SUCCESS: Added {name} to Notion.")
    else:
        print(f"ERROR: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test call
    # add_project_to_notion("BMS.auto-chatlog", "Aktiv", "BMS", "v3 fungerer")
    print("Sync logic ready.")
