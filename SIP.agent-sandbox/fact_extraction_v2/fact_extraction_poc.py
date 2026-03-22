import json
import os
import re
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

DIGEST_PATH = os.path.join(PROJECT_ROOT, "BMS.auto-chatlog/sections-digest.json")
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")
LEARNINGS_PATH = os.path.join(PROJECT_ROOT, "data/LEARNINGS.md")

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

    # 6. Læring/Lessons Learned (Gap 1 - WARM memory)
    if re.search(r"lærte|fejl|løsning|fungerede|virker nu|undgå", clean_text, re.I):
        sentences = re.split(r'[.!?]', clean_text)
        for s in sentences:
            s_clean = s.strip()
            if any(word in s_clean.lower() for word in ["lærte", "fejl", "løsning", "fungerede", "virker nu", "undgå"]):
                if len(s_clean) > 10:
                    facts.append({
                        "fact": s_clean,
                        "category": "learning",
                        "confidence": 0.8
                    })

    # 7. Evergreen / Fundamentale principper (Ny i S34)
    if any(p in clean_text.lower() for p in ["vision", "princip", "blueprint", "soul", "mandat", "identity"]):
        facts.append({
            "fact": f"Potentielt Evergreen-princip identificeret: {clean_text[:100]}...",
            "category": "evergreen",
            "confidence": 0.7,
            "is_evergreen": True
        })

    # Catch-all hvis teksten er lang nok (noget sker jo)
    if len(clean_text) > 100 and not facts:
         facts.append({
            "fact": "Generel aktivitet i sessionen.",
            "category": "activity",
            "confidence": 0.3
        })

    return facts

def update_learnings_file(facts):
    """Opdaterer data/LEARNINGS.md (WARM memory)."""
    learnings = [f for f in facts if f['category'] == 'learning']
    if not learnings:
        return

    new_content = ""
    if not os.path.exists(LEARNINGS_PATH):
        new_content = "# LEARNINGS (WARM Memory)\n\n"
    
    with open(LEARNINGS_PATH, 'a') as f:
        if new_content:
            f.write(new_content)
        for l in learnings:
            entry = f"- [{l['source_date']}] {l['fact']}\n"
            f.write(entry)

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

    new_facts = []
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
                new_facts.append(f)
            
    # Gem resultater
    os.makedirs(os.path.dirname(FACTS_PATH), exist_ok=True)
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
    
    # Opdater WARM memory (LEARNINGS.md)
    update_learnings_file(new_facts)
    
    print(f"Fact extraction færdig. {len(new_facts)} nye fakta fundet.")

if __name__ == "__main__":
    process_digest()
