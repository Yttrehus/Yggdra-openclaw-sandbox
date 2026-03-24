import json
import os
import sys
import subprocess
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

DIGEST_PATH = os.path.join(PROJECT_ROOT, "BMS.auto-chatlog/sections-digest.json")
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def get_latest_digest_text():
    if not os.path.exists(DIGEST_PATH):
        return None
            
    with open(DIGEST_PATH, 'r') as f:
        try:
            digest = json.load(f)
        except json.JSONDecodeError:
            return None
            
    if not digest.get('sections'):
        return None
    
    # Tag den seneste sektion (eller den der passer til i dag)
    latest = digest['sections'][-1]
    
    # Vi inkluderer også sessions-id og context for at hjælpe extractor
    context_text = f"Context: Session ongoing. Section ID: {latest['id']}. Date: {latest['date']}.\n"
    combined_text = context_text + " ".join(latest.get('userSamples', []) + latest.get('assistantSamples', []))
    
    # Simulation: Hvis vi er i Session 35, sørger vi for at extractor ved det
    if "Session 35" not in combined_text:
        combined_text += " [SYSTEM NOTE: This is Session 35, working on Notion and Retrieval v2.1]"
        
    return combined_text, latest['id'], latest['date']

def run_extraction_pipeline():
    print("--- Fact Extraction Pipeline v2.1 (LLM-Enhanced) ---")
    
    res = get_latest_digest_text()
    if not res:
        print("Error: No digest text found to process.")
        return
        
    text, sid, date = res
    print(f"Processing Section {sid} from {date}...")

    # 1. Kald subagent_extractor (simuleret LLM)
    process = subprocess.Popen(
        [sys.executable, os.path.join(SCRIPT_DIR, "subagent_extractor.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=text)
    
    if stderr:
        print(f"Extractor Stderr: {stderr}")

    try:
        new_facts = json.loads(stdout)
    except json.JSONDecodeError:
        print(f"Error parsing extractor output. Raw output: {stdout}")
        return

    if not new_facts:
        print("No new facts extracted.")
        return

    # 2. Indlæs eksisterende
    all_facts = []
    if os.path.exists(FACTS_PATH):
        try:
            with open(FACTS_PATH, 'r') as f:
                all_facts = json.load(f)
        except:
            all_facts = []

    # 3. Merge og de-duplikering
    added_count = 0
    for f in new_facts:
        f['timestamp'] = datetime.now().isoformat()
        f['section_id'] = sid
        f['source_date'] = date
        f['method'] = 'llm_v2'
        
        # De-duplikering baseret på tekst (case-insensitive)
        fact_text = f['fact'].strip()
        if not any(existing['fact'].lower() == fact_text.lower() for existing in all_facts):
            all_facts.append(f)
            added_count += 1
            print(f"  [NEW FACT] {fact_text}")
        else:
            print(f"  [STALE] {fact_text[:50]}...")

    # 4. Gem
    with open(FACTS_PATH, 'w') as f:
        json.dump(all_facts, f, indent=2)
        
    print(f"\nPipeline finished. Added {added_count} new facts to data/extracted_facts.json.")

if __name__ == "__main__":
    run_extraction_pipeline()
