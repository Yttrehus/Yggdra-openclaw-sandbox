#!/usr/bin/env python3
"""
Memory Re-indexer v1.0
Fokus: Validering og re-indeksering af fakta før ingestion til Qdrant.
Bruger "Vidar"-logik fra multi-agent simulationen.
"""
import os
import json
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
BACKUP_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.bak.json")

def reindex_facts():
    print("--- Memory Re-indexer (Vidar Logic) ---")
    if not os.path.exists(FACTS_FILE):
        print("Ingen faktafil fundet.")
        return

    # 1. Backup eksisterende hukommelse
    with open(FACTS_FILE, 'r') as f:
        facts = json.load(f)
    
    with open(BACKUP_FILE, 'w') as f:
        json.dump(facts, f, indent=2)
    print(f"Backup oprettet: {os.path.relpath(BACKUP_FILE, _PROJECT_ROOT)}")

    # 2. Vidar Logik: Validering & Rensning
    cleaned_facts = []
    duplicates = 0
    seen_texts = set()

    for fact in facts:
        text = fact.get('fact', '').strip()
        if not text: continue
        
        # Simpel de-duplikering
        if text in seen_texts:
            duplicates += 1
            continue
        
        seen_texts.add(text)
        
        # Kvalitets-tjek: Skal have en kategori og rimelig confidence
        if not fact.get('category'):
            fact['category'] = 'uncategorized'
        
        if fact.get('confidence', 0) < 0.5:
            # Markér for manuel revision i stedet for at slette (Lag 3 handling)
            fact['review_required'] = True
            
        cleaned_facts.append(fact)

    # 3. Gem re-indekseret hukommelse
    with open(FACTS_FILE, 'w') as f:
        json.dump(cleaned_facts, f, indent=2)

    print(f"Re-indeksering fuldført:")
    print(f"  - Behandlede fakta: {len(facts)}")
    print(f"  - Fjernede duplikater: {duplicates}")
    print(f"  - Validerede fakta: {len(cleaned_facts)}")

if __name__ == "__main__":
    reindex_facts()
