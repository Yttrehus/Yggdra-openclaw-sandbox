#!/usr/bin/env python3
"""
Episode Semantic Search v1.0
Fokus: Semantisk søgning over historiske hændelser (data/episodes.jsonl).
Del af V6.1 Hukommelses-evolution (Historisk bevidsthed).
"""
import json
import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODES_FILE = os.path.join(_PROJECT_ROOT, "data/episodes.jsonl")

def search_episodes(query):
    print(f"--- Episode Search: '{query}' ---")
    results = []
    if not os.path.exists(EPISODES_FILE):
        print("Ingen episode-log fundet.")
        return results

    # Simuleret semantisk match (keyword-baseret i denne PoC)
    keywords = query.lower().split()
    
    with open(EPISODES_FILE, "r") as f:
        for line in f:
            try:
                episode = json.loads(line)
                # Søg i alle tekst-felter (event, description osv.)
                content = str(episode.get("event", "")) + str(episode.get("description", ""))
                if any(k in content.lower() for k in keywords):
                    results.append(episode)
            except:
                continue
    
    return results

if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "session_end"
    found = search_episodes(q)
    for r in found[-5:]: # Vis seneste 5 matches
        print(f"[{r.get('timestamp')}] Event: {r.get('event')}")
