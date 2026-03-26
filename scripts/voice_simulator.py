import os
import sys
import time
import random
import json
from datetime import datetime

# Pathing
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")

def load_facts():
    if os.path.exists(FACTS_FILE):
        try:
            with open(FACTS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading facts: {e}")
    return []

def get_fact_chunks(query):
    facts = load_facts()
    if not facts:
        return ["Jeg kunne ikke indlæse fakta fra databasen.", "Tjek venligst data/extracted_facts.json."]
    
    # Simpel filter baseret på query ord (mocking retrieval)
    keywords = query.lower().split()
    relevant = [f['fact'] for f in facts if any(k in f['fact'].lower() for k in keywords)]
    
    if not relevant:
        # Fallback til de 3 nyeste fakta
        relevant = [f['fact'] for f in sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]]
        prefix = "Jeg fandt ikke specifikke matches, men her er det nyeste fra min hukommelse:"
    else:
        prefix = f"Jeg har fundet {len(relevant)} relevante fakta om det emne."

    return [prefix] + relevant[:3] + ["Skal jeg dykke dybere ned i nogle af dem?"]

def thinking_out_loud_sim(user_query):
    # 1. Acknowledge hurtigt (The 300ms Rule)
    print(f"\n[USER]: {user_query}")
    time.sleep(0.3)
    
    acknowledgements = [
        "Lad mig tjekke min hukommelse...",
        "Jeg kigger lige i de udtrukne fakta...",
        "Et øjeblik, jeg henter data...",
        "Lad mig se hvad jeg ved om det..."
    ]
    
    print(f"[VOICE - ACK]: {random.choice(acknowledgements)}")
    
    # 2. Simulerer LLM "deep thinking" latency (Data Retrieval)
    print("[... Deep Thinking (LLM & Fact Retrieval) ...]")
    time.sleep(1.5)
    
    # 3. Hent faktiske data fra disken
    response_chunks = get_fact_chunks(user_query)
    
    # 4. Leverer svaret i korte bidder (chunks for hurtigere TTS start)
    for chunk in response_chunks:
        print(f"[VOICE - CHUNK]: {chunk}")
        # Simulerer TTS afspilnings-tid per chunk (ca. 4 ord pr sekund)
        delay = len(chunk.split()) * 0.25 + 0.5
        time.sleep(delay)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "status"
    thinking_out_loud_sim(query)
