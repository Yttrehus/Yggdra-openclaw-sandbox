#!/usr/bin/env python3
"""
Yggdra V12.1.2 Neural Swarm Conflict Resolution
Fokus: Håndtering og løsning af modstridende fakta fra forskellige instanser.
"""
import os
import json
from datetime import datetime, timezone
import vidar_security_scan

class SwarmConflictResolver:
    def __init__(self, fact_file="data/extracted_facts.json"):
        self.fact_file = fact_file

    def resolve_conflicts(self, incoming_facts):
        print("--- Yggdra V12.1.2: Neural Swarm Conflict Resolution ---")
        
        # 1. Vidar Security Scan (V8)
        payload = {"incoming_count": len(incoming_facts)}
        is_safe, msg = vidar_security_scan.scan_api_call(
            service="ConflictResolver", 
            action="Resolve", 
            payload=payload,
            model="google/gemini-1.5-flash"
        )
        
        if not is_safe:
            print(f"[BLOCK]: {msg}")
            return False

        # 2. Hent eksisterende fakta
        existing_facts = []
        if os.path.exists(self.fact_file):
            with open(self.fact_file, "r") as f:
                existing_facts = json.load(f)

        resolved_facts = existing_facts.copy()
        conflicts_detected = 0

        # 3. Simuleret konfliktløsning (Temporal priority + Confidence)
        for incoming in incoming_facts:
            conflict_found = False
            for i, existing in enumerate(resolved_facts):
                # Simpel match-logik på emne (f.eks. "Notion API Status")
                if incoming.get("subject") == existing.get("subject"):
                    conflict_found = True
                    conflicts_detected += 1
                    print(f"[CONFLICT]: Modstridende info fundet for '{incoming['subject']}'.")
                    
                    # Beslutning: Nyere timestamp + højere confidence vinder
                    if incoming["timestamp"] > existing["timestamp"] and incoming["confidence"] >= existing["confidence"]:
                        print(f"[RESOLVE]: Indkommende fakta vinder (Nyere/Højere tillid).")
                        resolved_facts[i] = incoming
                    else:
                        print(f"[RESOLVE]: Eksisterende fakta bevares.")
            
            if not conflict_found:
                resolved_facts.append(incoming)

        # 4. Gem resultater
        with open(self.fact_file, "w") as f:
            json.dump(resolved_facts, f, indent=2)

        print(f"[SUCCESS]: Konfliktløsning færdig. {conflicts_detected} konflikter håndteret.")
        return True

if __name__ == "__main__":
    resolver = SwarmConflictResolver()
    # Test data
    mock_incoming = [
        {
            "subject": "Notion API Status",
            "fact": "VPS-Cloud rapporterer: API er online.",
            "confidence": 0.99,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "source": "VPS-Cloud"
        }
    ]
    resolver.resolve_conflicts(mock_incoming)
