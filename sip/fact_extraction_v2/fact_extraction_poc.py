import json
import os
import re
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

DIGEST_PATH = os.path.join(PROJECT_ROOT, "BMS.auto-chatlog/sections-digest.json")
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def clean_undefined(text):
    """Fjerner [undefined] artefakter og andre støj-elementer."""
    if not text: return ""
    text = re.sub(r'\[undefined\]', '', text)
    text = re.sub(r'undefined', '', text)
    text = re.sub(r'\[\s*\w?\s*\]', '', text)
    return text.strip()

def extract_facts_heuristic(text):
    """
    Simulerer Gap 6: Fact Extraction.
    """
    facts = []
    clean_text = clean_undefined(text)
    
    # 1. Ruter
    if re.search(r"rute", clean_text, re.I):
        facts.append({
            "fact": "Kontekst involverer transportruter.",
            "category": "work",
            "confidence": 0.5
        })

    # 2. Sessioner/Agent aktivitet
    if "Session" in clean_text or "agent" in clean_text.lower():
        facts.append({
            "fact": "Sessionen indeholder agent-aktivitetslogs.",
            "category": "meta",
            "confidence": 0.6
        })

    # 3. Gap/Retrieval
    if "Gap" in clean_text or "retrieval" in clean_text.lower():
        facts.append({
            "fact": "Sessionen diskuterer arkitektoniske gaps eller retrieval.",
            "category": "research",
            "confidence": 0.7
        })

    # 4. Specifikke beslutninger (PoC relateret)
    if "temporal decay" in clean_text.lower():
        facts.append({
            "fact": "Agenten arbejder på temporal decay PoC.",
            "category": "action",
            "confidence": 0.9
        })

    # 5. Beslutninger/Valg
    if re.search(r"besluttet|valgt|prioriteret", clean_text, re.I):
        facts.append({
            "fact": f"Beslutning identificeret: {clean_text[:100]}...",
            "category": "action",
            "confidence": 0.75
        })

    # Catch-all hvis teksten er lang nok (noget sker jo)
    if len(clean_text) > 100 and not facts:
         facts.append({
            "fact": "Generel aktivitet i sessionen.",
            "category": "activity",
            "confidence": 0.3
        })

    return facts

def process_digest():
    """Hovedloop for fact extraction."""
    if not os.path.exists(DIGEST_PATH):
        print(f"Fejl: Fandt ikke {DIGEST_PATH}")
        return

    with open(DIGEST_PATH, 'r') as f:
        try:
            digest = json.load(f)
        except json.JSONDecodeError:
            print(f"Fejl: Kunne ikke parse {DIGEST_PATH}")
            return

    all_facts = []
    
    # Indlæs eksisterende fakta hvis filen findes
    if os.path.exists(FACTS_PATH):
        try:
            with open(FACTS_PATH, 'r') as f:
                all_facts = json.load(f)
        except:
            all_facts = []

    new_facts_count = 0
    for section in digest.get('sections', []):
        combined_text = " ".join(section.get('userSamples', []) + section.get('assistantSamples', []))
        found = extract_facts_heuristic(combined_text)
        
        for f in found:
            f['timestamp'] = datetime.now().isoformat()
            f['section_id'] = section['id']
            f['source_date'] = section['date']
            # Simpel de-duplikering baseret på tekst
            if not any(existing['fact'] == f['fact'] for existing in all_facts):
                all_facts.append(f)
                new_facts_count += 1
            
    # Gem resultater
    os.makedirs(os.path.dirname(FACTS_PATH), exist_ok=True)
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    print(f"Fact extraction færdig. {new_facts_count} nye fakta fundet.")

if __name__ == "__main__":
    process_digest()
