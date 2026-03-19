import json
import os
import re

# Stier baseret på Yggdra struktur (scripts bor i sip/fact_extraction_v2/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def clean_fact_text(text):
    """Fjerner artefakter og rydder op i grammatik/stavefejl."""
    text = re.sub(r'\[\s*undefined\s*\]', '', text, flags=re.I)
    text = re.sub(r'undefined', '', text, flags=re.I)
    text = re.sub(r'\s+', ' ', text).strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    if text and not text.endswith(('.', '!', '?')):
        text += '.'
    return text

def clean_facts():
    """Gennemgår alle fakta og rydder op i deres tekst."""
    if not os.path.exists(FACTS_PATH):
        print(f"Fejl: Fandt ikke {FACTS_PATH}")
        return

    with open(FACTS_PATH, 'r') as f:
        try:
            facts = json.load(f)
        except json.JSONDecodeError:
            return

    print(f"--- Renser {len(facts)} fakta ---")
    
    changes = 0
    for f in facts:
        old_text = f.get('fact', '')
        new_text = clean_fact_text(old_text)
        if old_text != new_text:
            f['fact'] = new_text
            changes += 1

    if changes > 0:
        with open(FACTS_PATH, 'w') as f:
            json.dump(facts, f, indent=2)
        print(f"Rensning færdig. {changes} fakta opdateret.")
    else:
        print("Ingen ændringer nødvendige.")

if __name__ == "__main__":
    clean_facts()
