import os
import sys
import argparse
import re
import json
import requests
from datetime import datetime

# Notion API Client
class NotionClient:
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def get_page_id_by_name(self, project_name):
        """Finder page ID for et eksisterende projekt i databasen."""
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        payload = {
            "filter": {
                "property": "Navn",
                "title": {"equals": project_name}
            }
        }
        try:
            resp = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                return results[0]["id"] if results else None
        except Exception as e:
            print(f"Error querying Notion: {e}")
        return None

    def push_update(self, project, status, confidence=None):
        """Pusher status-opdatering til Notion (Update eller Create)."""
        page_id = self.get_page_id_by_name(project)
        now_iso = datetime.now().strftime("%Y-%m-%d")
        
        properties = {
            "Status": {"select": {"name": "Aktiv"}},
            "Næste Step": {"rich_text": [{"text": {"content": status}}]},
            "Sidst Opdateret": {"date": {"start": now_iso}}
        }
        
        if confidence is not None:
            # Vi bruger rich_text til Confidence indtil vi ved om det er et Number i DB
            # Tilføjer stjerne-rating for visuel feedback (v1.2)
            stars = "⭐" * int(confidence * 5)
            properties["Confidence"] = {"rich_text": [{"text": {"content": f"{confidence:.2f} {stars}"}}]}

        if page_id:
            # Opdater eksisterende side
            url = f"https://api.notion.com/v1/pages/{page_id}"
            payload = {"properties": properties}
            resp = requests.patch(url, json=payload, headers=self.headers, timeout=10)
        else:
            # Opret ny side
            url = "https://api.notion.com/v1/pages"
            properties["Navn"] = {"title": [{"text": {"content": project}}]}
            payload = {
                "parent": {"database_id": self.database_id},
                "properties": properties
            }
            resp = requests.post(url, json=payload, headers=self.headers, timeout=10)
            
        if resp.status_code in (200, 201):
            print(f"  [SUCCESS] {project} updated.")
        else:
            print(f"  [ERROR] {project} failed: {resp.status_code} - {resp.text}")

# Dry Run Client til brug uden API-nøgle
class DryRunClient:
    def __init__(self):
        self.updates = []
        self.output_path = "data/notion_dry_run.json"

    def push_update(self, project, status, confidence=None):
        update = {
            "project": project,
            "status": status,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        self.updates.append(update)
        stars = "⭐" * int(confidence * 5) if confidence else ""
        conf_str = f" (Conf: {confidence:.2f} {stars})" if confidence else ""
        print(f"  [DRY RUN] {project}: {status}{conf_str}")

    def finalize(self):
        with open(self.output_path, "w") as f:
            json.dump(self.updates, f, indent=2)
        print(f"  [DRY RUN] Results saved to {self.output_path}")

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
            if line.startswith("##") or not line.strip():
                if projects:
                    break
                continue
            match = re.search(r"- \*\*([\w\.\-]+):\*\* (.*)", line)
            if match:
                projects.append({
                    "name": match.group(1),
                    "status": match.group(2).strip()
                })
    return projects

def get_project_confidence(project_name):
    """Beregner gennemsnitlig confidence for et projekt baseret på extracted_facts.json."""
    facts_path = "data/extracted_facts.json"
    if not os.path.exists(facts_path): return None
    
    try:
        with open(facts_path, 'r') as f:
            facts = json.load(f)
        
        # Simpel matching: tjek om projektnavn (eller dele af det) findes i faktum eller metadata
        relevant_confidences = [f['confidence'] for f in facts if project_name.lower() in f['fact'].lower() and 'confidence' in f]
        
        if relevant_confidences:
            return sum(relevant_confidences) / len(relevant_confidences)
    except:
        pass
    return None

def sync_to_notion(dry_run=False):
    """Syncs current project status from CONTEXT.md to Notion."""
    print(f"--- Notion Sync Engine v1.2 ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---")
    token = os.environ.get("NOTION_API_KEY")
    db_id = os.environ.get("NOTION_DATABASE_ID")
    
    projects = extract_status_from_context()
    if not projects:
        print("No active projects found in CONTEXT.md.")
        return

    if dry_run or not token or not db_id:
        if not dry_run:
            print("NOTION_API_KEY or NOTION_DATABASE_ID not found. Forcing DRY RUN.")
        else:
            print("DRY RUN mode active.")
        client = DryRunClient()
    else:
        print("Notion credentials found. Attempting live sync...")
        client = NotionClient(token, db_id)

    for p in projects:
        conf = get_project_confidence(p['name'])
        client.push_update(p['name'], p['status'], confidence=conf)
    
    if isinstance(client, DryRunClient):
        client.finalize()
        
    print("STATUS: Sync complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-end", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    if args.session_end or args.dry_run:
        sync_to_notion(dry_run=args.dry_run)
