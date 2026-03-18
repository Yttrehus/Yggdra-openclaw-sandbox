import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_PATH = os.path.join(PROJECT_ROOT, "../../data/extracted_facts.json")

def validate_facts():
    """Validerer ekstraherede fakta for kvalitet, duplikater og kategorisering."""
    if not os.path.exists(FACTS_PATH):
        print(f"Fejl: Fandt ikke {FACTS_PATH}")
        return

    try:
        with open(FACTS_PATH, 'r') as f:
            facts = json.load(f)
    except json.JSONDecodeError:
        print("Fejl: Kunne ikke parse extracted_facts.json")
        return

    print(f"--- Validerer {len(facts)} fakta ---")
    
    validated = []
    issues = 0

    # Definer gyldige kategorier (baseret på GAPS.md og topics)
    VALID_CATEGORIES = ['work', 'action', 'research', 'meta', 'activity', 'office']

    for f in facts:
        fact_text = f.get('fact', '').strip()
        category = f.get('category', 'unknown').lower()
        
        # 1. Kvalitetskrav: Længde
        if len(fact_text) < 10:
            print(f"Issue [Længde]: Faktum for kort: '{fact_text}'")
            issues += 1
            continue
            
        # 2. Kvalitetskrav: Kategorisering
        if category not in VALID_CATEGORIES:
            print(f"Issue [Kategori]: Ugyldig kategori '{category}' for: '{fact_text[:30]}...'")
            # Vi forsøger ikke at rette den her, men logger det
            issues += 1
            if category == 'unknown':
                f['category'] = 'activity' # Default fallback
        
        # 3. Tjek for duplikater (fuzzy-ish match: ignorér case og whitespace)
        is_duplicate = False
        normalized_fact = fact_text.lower()
        for v in validated:
            if v['fact'].lower() == normalized_fact:
                is_duplicate = True
                break
        
        if is_duplicate:
            print(f"Issue [Duplikat]: Fjernet duplikat: '{fact_text[:50]}...'")
            issues += 1
            continue

        validated.append(f)

    # Gem validerede fakta tilbage
    with open(FACTS_PATH, 'w') as f:
        json.dump(validated, f, indent=2)

    print(f"Validering færdig. {issues} issues adresseret. {len(validated)} fakta bevaret.")

if __name__ == "__main__":
    validate_facts()
