import json
import os
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))

FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")
MEMORY_PATH = os.path.join(PROJECT_ROOT, "MEMORY.md")

def reflect_on_knowledge():
    """Giver et kort overblik over den akkumulerede viden i denne session."""
    if not os.path.exists(FACTS_PATH):
        return

    with open(FACTS_PATH, 'r') as f:
        facts = json.load(f)

    if not facts:
        return

    # Find fakta fra den absolut seneste sektion
    sorted_facts = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)
    latest_section_id = sorted_facts[0].get('section_id')
    latest_facts = [f for f in sorted_facts if f.get('section_id') == latest_section_id]

    print("\n=== AGENT SELF-REFLECTION ===")
    print(f"Session-id: {latest_section_id}")
    print(f"Ekstraheret viden: {len(latest_facts)} punkter")
    
    categories = {}
    for f in latest_facts:
        cat = f['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("Kategorier: " + ", ".join([f"{k.upper()}({v})" for k, v in categories.items()]))
    
    # Foreslå opdateringer til MEMORY.md hvis der er vigtige handlinger
    actions = [f for f in latest_facts if f['category'] == 'action']
    if actions:
        print("\nVigtige handlinger fundet:")
        for a in actions:
            print(f"- {a['fact']}")
    
    print("==============================\n")

if __name__ == "__main__":
    reflect_on_knowledge()
