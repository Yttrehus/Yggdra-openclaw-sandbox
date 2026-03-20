import json
import os
import re
from datetime import datetime

# Stier baseret på Yggdra struktur (scripts bor i sip/fact_extraction_v2/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")
MEMORY_PATH = os.path.join(PROJECT_ROOT, "MEMORY.md")
MEMORY_INGEST_DIR = os.path.join(PROJECT_ROOT, "sip/memory_ingest")

def merge_to_memory():
    """Forsøger at merge validerede fakta ind i MEMORY.md og genererer Fact Sheets til Qdrant."""
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

    # Sorter fakta efter timestamp for at finde de nyeste
    sorted_facts = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)
    if not sorted_facts:
        return
        
    latest_section_id = sorted_facts[0].get('section_id')
    recent_facts = [f for f in sorted_facts if f.get('section_id') == latest_section_id]

    print(f"--- Behandler {len(recent_facts)} nylige fakta ---")

    # 1. Update MEMORY.md
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'r') as f:
            memory_content = f.read()
    else:
        memory_content = "# MEMORY\n\n## Autonome Indsigter\n"

    new_memory_entries = []
    for f in recent_facts:
        # Undgå duplikater i MEMORY.md (simpel streng-match)
        if f['fact'] not in memory_content:
            entry = f"- [{f['category'].upper()}] {f['fact']} (Kilde: {f['source_date']})"
            new_memory_entries.append(entry)

    if new_memory_entries:
        # Hvis headeren mangler i den eksisterende fil
        if "## Autonome Indsigter" not in memory_content:
            with open(MEMORY_PATH, 'a') as f:
                f.write("\n\n## Autonome Indsigter\n")
        
        with open(MEMORY_PATH, 'a') as f:
            for entry in new_memory_entries:
                f.write(entry + "\n")
        print(f"MEMORY.md: {len(new_memory_entries)} nye indlæg tilføjet.")
    else:
        print("MEMORY.md: Ingen nye unikke fakta fundet.")

    # 2. Generer Fact Sheets til Memory Ingest (Qdrant)
    os.makedirs(MEMORY_INGEST_DIR, exist_ok=True)
    
    timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M")
    fact_sheet_path = os.path.join(MEMORY_INGEST_DIR, f"fact_sheet_{timestamp_slug}.md")
    
    with open(fact_sheet_path, 'w') as f:
        f.write(f"# Fact Sheet — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"Dette dokument indeholder atomiske fakta ekstraheret autonomt i session {latest_section_id}.\n\n")
        f.write("## Ekstraherede fakta\n\n")
        for fact in recent_facts:
            f.write(f"### {fact['category'].upper()}\n")
            f.write(f"- **Faktum:** {fact['fact']}\n")
            f.write(f"- **Kilde dato:** {fact['source_date']}\n")
            f.write(f"- **Confidence:** {fact.get('confidence', 0.0):.2f}\n\n")

    print(f"Fact Sheet genereret: {fact_sheet_path}")

if __name__ == "__main__":
    merge_to_memory()
