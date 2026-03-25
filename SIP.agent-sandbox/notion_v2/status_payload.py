import os
import json
import re

def get_projects_payload():
    context_path = "CONTEXT.md"
    if not os.path.exists(context_path):
        return None
        
    with open(context_path, "r") as f:
        content = f.read()
        
    projects = []
    # Targeted search within the "### Aktive projekter" section with looser matching
    # First, find the start of the section
    lines = content.split('\n')
    start_idx = -1
    for i, line in enumerate(lines):
        if "### Aktive projekter" in line:
            start_idx = i
            break
            
    if start_idx != -1:
        # Scan until next header or end of file
        for line in lines[start_idx+1:]:
            if line.startswith("##"):
                break
            match = re.search(r"- \*\*([\w\.\-]+):\*\* (.*)", line)
            if match:
                projects.append({
                    "name": match.group(1),
                    "status": match.group(2).strip()
                })
    
    return {
        "source": "Yggdra PC",
        "last_sync": "2026-03-24",
        "projects": projects
    }

if __name__ == "__main__":
    payload = get_projects_payload()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
