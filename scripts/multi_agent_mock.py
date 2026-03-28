#!/usr/bin/env python3
"""
Multi-Agent Orchestration Mock v1.0
Fokus: Simulation af samarbejde mellem specialiserede sub-agenter.
Del af Lag 3 (Handling).
"""
import time
import random

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def execute(self, task):
        print(f"[{self.name} - {self.role}]: Arbejder på '{task}'...")
        time.sleep(random.uniform(1.0, 2.5))
        return f"Resultat fra {self.name}"

def orchestrate_sync_and_extraction():
    researcher = Agent("Hugin", "Epistemisk Scanner")
    extractor = Agent("Munin", "Semantisk Arkivar")
    
    print("--- Multi-Agent Orchestration Simulation ---")
    
    # Task 1: Scan for ny viden
    discovery = researcher.execute("Scan ai_intelligence for nye mønstre")
    print(f"  -> {discovery}")
    
    # Task 2: Udfør extraction
    facts = extractor.execute(f"Udtræk fakta baseret på {discovery}")
    print(f"  -> {facts}")
    
    print("\n[ORCHESTRATOR]: Samarbejde fuldført. Hukommelse opdateret.")

if __name__ == "__main__":
    orchestrate_sync_and_extraction()
