import json
import os
import sys
from datetime import datetime

# Stier baseret på Yggdra struktur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
FACTS_PATH = os.path.join(PROJECT_ROOT, "data/extracted_facts.json")

def check_for_alerts():
    """Tjekker efter nylige høj-prioritets fakta der kræver opmærksomhed."""
    if not os.path.exists(FACTS_PATH):
        return

    with open(FACTS_PATH, 'r') as f:
        try:
            facts = json.load(f)
        except json.JSONDecodeError:
            return

    if not facts:
        return

    # Sorter fakta efter timestamp for at finde de nyeste
    sorted_facts = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Find fakta fra den seneste sektion (som simulerer "denne session")
    latest_section_id = sorted_facts[0].get('section_id')
    recent_facts = [f for f in sorted_facts if f.get('section_id') == latest_section_id]
    
    # Filtrer for kategorier der fortjener en alert
    alerts = [f for f in recent_facts if f.get('category') in ['action', 'work', 'research']]
    
    if alerts:
        print("\n" + "="*50)
        print("🔔 PROAKTIVE AGENT NOTIFIKATIONER")
        print("="*50)
        for a in alerts:
            cat = a['category'].upper()
            fact = a['fact']
            conf = a.get('confidence', 0.0)
            print(f"[{cat}] ({conf:.2f}) > {fact}")
        print("="*50 + "\n")
        
        # Integration med OpenClaw sessions_send (simuleret her via stdout)
        # I en aktiv agent session kan vi bruge dette til at 'vække' ejeren
        # eller sende til en specifik kanal hvis konfigureret.

if __name__ == "__main__":
    check_for_alerts()
