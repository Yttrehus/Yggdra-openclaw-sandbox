import json
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_PATH = os.path.join(PROJECT_ROOT, "../../data/extracted_facts.json")

def clean_fact_text(text):
    """Fjerner artefakter og rydder op i grammatik/stavefejl."""
    # Fjern rester af [undefined] hvis de slap igennem
    text = re.sub(r'\[\s*undefined\s*\]', '', text, flags=re.I)
    text = re.sub(r'undefined', '', text, flags=re.I)
    
    # Fjern dobbelte mellemrum
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Sørg for at det starter med stort og slutter med punktum
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
        facts = json.load(f)

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
