import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_PATH = os.path.join(PROJECT_ROOT, "../../data/extracted_facts.json")
MEMORY_PATH = os.path.join(PROJECT_ROOT, "../../MEMORY.md")

def merge_to_memory():
    """Forsøger at merge validerede fakta ind i MEMORY.md."""
    if not os.path.exists(FACTS_PATH):
        print(f"Fejl: Fandt ikke {FACTS_PATH}")
        return

    with open(FACTS_PATH, 'r') as f:
        facts = json.load(f)

    if not facts:
        print("Ingen fakta at merge.")
        return

    print(f"--- Merger {len(facts)} fakta til MEMORY.md ---")
    
    # Læs MEMORY.md
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'r') as f:
            memory_content = f.read()
    else:
        memory_content = "# MEMORY\n\n## Autonome Indsigter\n"

    new_entries = []
    for f in facts:
        # Tjek om faktum allerede findes i MEMORY.md (simpel streng-match)
        if f['fact'] not in memory_content:
            entry = f"- [{f['category'].upper()}] {f['fact']} (Kilde: {f['source_date']})"
            new_entries.append(entry)

    if new_entries:
        with open(MEMORY_PATH, 'a') as f:
            if "\n## Autonome Indsigter" not in memory_content:
                f.write("\n\n## Autonome Indsigter\n")
            for entry in new_entries:
                f.write(entry + "\n")
        print(f"Success: {len(new_entries)} nye indlæg tilføjet til MEMORY.md")
    else:
        print("Ingen nye unikke fakta fundet.")

if __name__ == "__main__":
    merge_to_memory()
