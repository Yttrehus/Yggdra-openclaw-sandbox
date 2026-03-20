import json
import os
import sys
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def inject_facts_from_subagent(json_data, section_id, source_date):
    """
    Modtager JSON data fra en subagent turn og gemmer det i extracted_facts.json.
    Dette fungerer som broen mellem subagentens 'thinking' og filsystemet.
    """
    try:
        new_facts = json.loads(json_data)
    except json.JSONDecodeError:
        print("Fejl: Kunne ikke parse JSON fra subagent.")
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
        f['method'] = 'subagent_bridge'
        
        # De-duplikering baseret på fakta-tekst
        if not any(existing['fact'] == f['fact'] for existing in all_facts):
            all_facts.append(f)
            added_count += 1
            
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    return added_count

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Brug: python3 agent_bridge.py '<json_data>' <section_id> <source_date>")
        sys.exit(1)
    
    json_input = sys.argv[1]
    sid = int(sys.argv[2])
    sdate = sys.argv[3]
    
    count = inject_facts_from_subagent(json_input, sid, sdate)
    print(f"SUCCESS: {count} fakta injiceret via broen.")
