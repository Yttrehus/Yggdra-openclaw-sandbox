import json
import os
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))

FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")
MEMORY_PATH = os.path.join(PROJECT_ROOT, "MEMORY.md")

def merge_to_memory():
    """Forsøger at merge validerede fakta ind i MEMORY.md."""
    if not os.path.exists(FACTS_PATH):
        print(f"Fejl: Fandt ikke {FACTS_PATH}")
        return

    with open(FACTS_PATH, 'r') as f:
        try:
            facts = json.load(f)
        except json.JSONDecodeError:
            print("Fejl: Kunne ikke parse extracted_facts.json")
            return

    if not facts:
        print("Ingen fakta at merge.")
        return

    # Læs MEMORY.md
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'r') as f:
            memory_content = f.read()
    else:
        memory_content = "# MEMORY\n\n## Autonome Indsigter\n"

    new_entries = []
    # Vi kigger kun på de seneste fakta (fra denne session/sektion)
    # Sorter fakta efter timestamp for at finde de nyeste
    sorted_facts = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)
    if not sorted_facts:
        return
        
    latest_section_id = sorted_facts[0].get('section_id')
    recent_facts = [f for f in sorted_facts if f.get('section_id') == latest_section_id]

    print(f"--- Merger {len(recent_facts)} nylige fakta til MEMORY.md ---")
    
    for f in recent_facts:
        # Tjek om faktum allerede findes i MEMORY.md (simpel streng-match)
        if f['fact'] not in memory_content:
            entry = f"- [{f['category'].upper()}] {f['fact']} (Kilde: {f['source_date']})"
            new_entries.append(entry)

    if new_entries:
        # Hvis filen er tom eller mangler header
        if "## Autonome Indsigter" not in memory_content:
            with open(MEMORY_PATH, 'a') as f:
                f.write("\n## Autonome Indsigter\n")
        
        with open(MEMORY_PATH, 'a') as f:
            for entry in new_entries:
                f.write(entry + "\n")
        print(f"Success: {len(new_entries)} nye indlæg tilføjet til MEMORY.md")
    else:
        print("Ingen nye unikke fakta fundet.")

if __name__ == "__main__":
    merge_to_memory()
