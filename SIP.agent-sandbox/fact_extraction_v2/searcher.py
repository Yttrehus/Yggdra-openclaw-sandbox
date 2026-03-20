import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_PATH = os.path.join(PROJECT_ROOT, "../../data/extracted_facts.json")

def search_facts(query):
    """Søger i de ekstraherede fakta."""
    if not os.path.exists(FACTS_PATH):
        print(f"Fejl: Fandt ikke {FACTS_PATH}")
        return

    with open(FACTS_PATH, 'r') as f:
        facts = json.load(f)

    query = query.lower()
    results = []

    for f in facts:
        if query in f['fact'].lower() or query in f['category'].lower():
            results.append(f)

    if not results:
        print(f"Ingen fakta fundet for: '{query}'")
        return

    print(f"--- Fundet {len(results)} fakta for '{query}' ---")
    for r in results:
        print(f"[{r['category'].upper()}] (Confidence: {r['confidence']})")
        print(f"Fact: {r['fact']}")
        print(f"Dato: {r['source_date']}")
        print("-" * 20)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Brug: python3 searcher.py <søgeord>")
    else:
        search_facts(sys.argv[1])
