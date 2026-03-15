import json
import re
from datetime import datetime

def extract_facts(text):
    """
    Simulerer Gap 6: Fact Extraction.
    I en rigtig implementation ville dette bruge en LLM (f.eks. Claude eller Groq)
    til at identificere atomiske fakta.
    """
    print("Extracting facts from text...")
    
    # Simuleret LLM logic: kig efter mønstre som "X er Y" eller "Husk Z"
    facts = []
    
    # Eksempel på hvad en LLM ville finde:
    if "rute 256" in text.lower():
        facts.append({
            "fact": "Rute 256 handler om opsamling af organisk affald i Aarhus.",
            "source_type": "chat_session",
            "confidence": 0.95,
            "category": "work"
        })
    
    if "kaffemaskine" in text.lower() and "stykker" in text.lower():
        facts.append({
            "fact": "Kaffemaskinen på kontoret er defekt.",
            "source_type": "chat_session",
            "confidence": 0.9,
            "category": "office"
        })
        
    return facts

def process_session_digest(digest_path):
    """Læser sektioner fra chatlog digest og ekstraherer fakta."""
    try:
        with open(digest_path, 'r') as f:
            digest = json.load(f)
    except FileNotFoundError:
        print(f"Fejl: Fandt ikke {digest_path}")
        return

    all_extracted_facts = []
    
    for section in digest.get('sections', []):
        print(f"Processing Section {section['id']} ({section['timeRange']})...")
        # Kombiner samples for at simulere fuld tekst
        combined_text = " ".join(section.get('userSamples', []) + section.get('assistantSamples', []))
        facts = extract_facts(combined_text)
        for f in facts:
            f['timestamp'] = datetime.now().isoformat()
            f['section_id'] = section['id']
            all_extracted_facts.append(f)
            
    return all_extracted_facts

if __name__ == "__main__":
    print("Yggdra Fact Extraction PoC - Closing Gap 6")
    
    # Vi bruger den digest fil som chatlog-engine genererer
    DIGEST_PATH = "projects/auto-chatlog/sections-digest.json"
    
    extracted = process_session_digest(DIGEST_PATH)
    
    if extracted:
        output_path = "data/extracted_facts.json"
        with open(output_path, 'w') as f:
            json.dump(extracted, f, indent=2)
        
        print(f"\nSUCCESS: Ekstraheret {len(extracted)} fakta.")
        print(f"Gemt i {output_path}")
        for f in extracted:
            print(f"- [{f['category'].upper()}] {f['fact']}")
