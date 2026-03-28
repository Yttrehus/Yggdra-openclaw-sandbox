import os
import requests
import json

# Forventer NOTION_API_KEY og PARENT_PAGE_ID i miljøet
NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
PARENT_PAGE = os.environ.get("PARENT_PAGE_ID")

def create_yggdra_projects_db():
    if not NOTION_TOKEN or not PARENT_PAGE:
        print("Error: NOTION_API_KEY or PARENT_PAGE_ID missing.")
        return

    url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE},
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
            "Confidence": {"rich_text": {}}, # Tilføjet til match med notion_sync.py v1.1
            "Sidst Opdateret": {"date": {}},
            "Mobil-Noter": {"rich_text": {}},
            "URL": {"url": {}}
        }
    }

    print(f"Initializing Notion database on parent page: {PARENT_PAGE}")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        db_id = response.json()['id']
        print(f"SUCCESS: Database created! ID: {db_id}")
        return db_id
    else:
        print(f"ERROR: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    create_yggdra_projects_db()
