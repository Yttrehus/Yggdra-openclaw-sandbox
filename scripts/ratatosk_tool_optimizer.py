#!/usr/bin/env python3
"""
Ratatosk Tool Optimizer v1.0
Fokus: Valg af værktøjer baseret på Vidars sikkerheds- og omkostnings-kriterier.
Del af V8 Collaborative Intelligence.
"""
import json
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICING_FILE = os.path.join(_PROJECT_ROOT, "data/llm_pricing.json")

def get_recommended_tools(task_type):
    print(f"--- Ratatosk: Optimerer værktøjsvalg for '{task_type}' ---")
    
    # Standard værktøjer
    tools = {
        "data_processing": ["pandas_mcp", "qdrant_mcp"],
        "notification": ["slack_mcp", "email_mcp"],
        "storage": ["filesystem_mcp", "s3_mcp"]
    }
    
    # Hent prisdata for at optimere efter omkostning
    if os.path.exists(PRICING_FILE):
        with open(PRICING_FILE, "r") as f:
            pricing = json.load(f)["pricing"]
        
        # Simuleret valg af billigste model til opgaven
        cheapest_model = min(pricing, key=pricing.get)
        print(f"[Ratatosk]: Anbefaler model '{cheapest_model}' pga. laveste omkostning.")
    
    recommended = tools.get(task_type, ["general_purpose_mcp"])
    
    # Vidar-betinget filtrering (simulation)
    if "purge" in task_type:
        print("[Ratatosk]: Opgave indeholder 'purge'. Vidar kræver begrænset adgang. Bruger 'safe_purge_mcp'.")
        recommended = ["safe_purge_mcp"]
        
    return recommended

if __name__ == "__main__":
    print(f"[RECOMMENDED]: {get_recommended_tools('data_processing')}")
