import json
import os
import sys
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

DIGEST_PATH = os.path.join(PROJECT_ROOT, "BMS.auto-chatlog/sections-digest.json")
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def get_latest_digest_text():
    path_to_try = DIGEST_PATH
    if not os.path.exists(path_to_try):
        path_to_try = os.path.join(PROJECT_ROOT, "BMS.auto-chatlog/sections-digest.json")
        
    if not os.path.exists(path_to_try):
        return None
            
    with open(path_to_try, 'r') as f:
        try:
            digest = json.load(f)
        except json.JSONDecodeError:
            return None
            
    if not digest.get('sections'):
        return None
    
    # Tag den seneste sektion
    latest = digest['sections'][-1]
    combined_text = " ".join(latest.get('userSamples', []) + latest.get('assistantSamples', []))
    return combined_text, latest['id'], latest['date']

def inject_subagent_facts(new_facts, section_id, source_date):
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
        f['method'] = 'subagent_direct'
        
        # De-duplikering
        if not any(existing['fact'] == f['fact'] for existing in all_facts):
            all_facts.append(f)
            added_count += 1
            
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
    return added_count

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        try:
            # Vi forventer metadata i args hvis --save bruges
            # Brug: --save <sid> <date>
            sid = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            sdate = sys.argv[3] if len(sys.argv) > 3 else "unknown"
            input_data = json.load(sys.stdin)
            count = inject_subagent_facts(input_data, sid, sdate)
            print(f"SUCCESS:{count}")
        except Exception as e:
            print(f"ERROR:{e}")
    else:
        res = get_latest_digest_text()
        if res:
            text, sid, date = res
            print(f"SECTION_ID:{sid}")
            print(f"SOURCE_DATE:{date}")
            print("---TEXT_START---")
            print(text)
            print("---TEXT_END---")
        else:
            print("ERROR: No digest found")
