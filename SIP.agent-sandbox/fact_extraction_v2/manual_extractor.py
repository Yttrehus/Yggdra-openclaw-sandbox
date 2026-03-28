import json
import os
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
FACTS_PATH = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
INTELLIGENCE_DIR = os.path.join(_PROJECT_ROOT, "data/intelligence")

def extract_manual():
    print("--- Manuel Fact Extraction (Recovery Mode) ---")
    
    if os.path.exists(FACTS_PATH):
        with open(FACTS_PATH, 'r') as f:
            facts = json.load(f)
    else:
        facts = []

    # Find seneste section_id
    latest_id = max([f.get('section_id', 0) for f in facts]) if facts else 0
    new_id = latest_id + 1

    intel_files = sorted(list(Path(INTELLIGENCE_DIR).glob("daily_*.md")))
    
    new_facts_count = 0
    for file in intel_files:
        date_str = file.stem.replace("daily_", "")
        # Tjek om vi allerede har fakta fra denne dato
        if any(f.get('source_date') == date_str for f in facts):
            continue
            
        print(f"Behandler {file.name}...")
        with open(file, 'r') as f:
            content = f.read()
            
        # Simpel extraction: Hent linjer fra Key Events
        lines = content.split('\n')
        in_events = False
        for line in lines:
            if "## Key Events" in line:
                in_events = True
                continue
            if line.startswith("##"):
                in_events = False
            
            if in_events and line.startswith("- **"):
                fact_text = line.replace("- **", "").strip()
                fact_text = fact_text.replace("**:", ":") # Rens formatering
                
                new_fact = {
                    "fact": fact_text,
                    "category": "intelligence",
                    "confidence": 0.9,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "section_id": new_id,
                    "source_date": date_str,
                    "method": "manual_recovery"
                }
                facts.append(new_fact)
                new_facts_count += 1

    if new_facts_count > 0:
        with open(FACTS_PATH, 'w') as f:
            json.dump(facts, f, indent=2)
        print(f"Succes: {new_facts_count} nye fakta tilføjet til extracted_facts.json")
    else:
        print("Ingen nye unikke fakta fundet i intelligence-filer.")

if __name__ == "__main__":
    extract_manual()
