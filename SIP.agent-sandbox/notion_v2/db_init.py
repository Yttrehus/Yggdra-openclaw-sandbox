import os
import requests
import json

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")

def create_projects_database(parent_page_id):
    if not NOTION_TOKEN:
        print("Error: NOTION_API_KEY missing.")
        return

    url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Yggdra Projekter"}}],
        "properties": {
            "Navn": {"title": {}},
            "Status": {"select": {"options": [
                {"name": "Aktiv", "color": "green"},
                {"name": "Pauset", "color": "yellow"},
                {"name": "Venter", "color": "orange"},
                {"name": "Arkiveret", "color": "gray"}
            ]}},
            "Stage": {"select": {"options": [
                {"name": "BMS", "color": "blue"},
                {"name": "LIB", "color": "purple"},
                {"name": "REF", "color": "pink"},
                {"name": "KNB", "color": "brown"},
                {"name": "DLR", "color": "red"},
                {"name": "SIP", "color": "orange"},
                {"name": "PoC", "color": "yellow"}
            ]}},
            "Næste Step": {"rich_text": {}},
            "Sidst Opdateret": {"date": {}},
            "Mobil-Noter": {"rich_text": {}}
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"SUCCESS: Database created! ID: {response.json()['id']}")
    else:
        print(f"ERROR: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Notion DB Init Script Ready.")
