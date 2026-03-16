import json
import os
import sys
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
DIGEST_PATH = os.path.join(PROJECT_ROOT, "projects/auto-chatlog/sections-digest.json")
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def get_latest_digest_text():
    if not os.path.exists(DIGEST_PATH):
        return None
    with open(DIGEST_PATH, 'r') as f:
        digest = json.load(f)
    if not digest.get('sections'):
        return None
    
    # Tag den seneste sektion
    latest = digest['sections'][-1]
    combined_text = " ".join(latest.get('userSamples', []) + latest.get('assistantSamples', []))
    return combined_text, latest['id'], latest['date']

def save_subagent_facts(new_facts, section_id, source_date):
    if not new_facts:
        return 0
        
    all_facts = []
    if os.path.exists(FACTS_PATH):
        try:
            with open(FACTS_PATH, 'r') as f:
                all_facts = json.load(f)
        except:
            all_facts = []
            
    added_count = 0
    for f in new_facts:
        f['timestamp'] = datetime.now().isoformat()
        f['section_id'] = section_id
        f['source_date'] = source_date
        f['method'] = 'subagent'
        
        # De-duplikering
        if not any(existing['fact'] == f['fact'] for existing in all_facts):
            all_facts.append(f)
            added_count += 1
            
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
    return added_count

if __name__ == "__main__":
    # Dette script er beregnet til at blive kaldt af hovedagenten
    # som derefter kører en subagent turn.
    res = get_latest_digest_text()
    if res:
        text, sid, date = res
        print(f"LATEST_TEXT_START")
        print(text)
        print(f"LATEST_TEXT_END")
        print(f"METADATA:{sid}:{date}")
