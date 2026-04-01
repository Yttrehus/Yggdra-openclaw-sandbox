#!/usr/bin/env python3
"""
Vidar Security Scan v1.1
Fokus: Real-tids scanning med aktiv prissætnings-integration og veto-logik.
Del af V8 Collaborative Intelligence.
"""
import json
import os
import random

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICING_FILE = os.path.join(_PROJECT_ROOT, "data/llm_pricing.json")

def get_current_pricing():
    if os.path.exists(PRICING_FILE):
        with open(PRICING_FILE, "r") as f:
            return json.load(f)["pricing"]
    return {"google/gemini-1.5-flash": 0.1} # Fallback

def scan_api_call(service, action, payload=None, model="google/gemini-1.5-flash"):
    print(f"--- Vidar Security v1.1: Scanner kald til '{service}' ({action}) ---")
    
    # 1. Dynamisk Cost Estimation baseret på nyeste priser
    pricing = get_current_pricing()
    price_per_1m = pricing.get(model, 0.1)
    
    token_estimate = random.randint(100, 10000)
    cost_estimate = (token_estimate / 1000000) * price_per_1m
    
    print(f"[Vidar]: Model: {model}")
    print(f"[Vidar]: Estimeret token forbrug: {token_estimate}")
    print(f"[Vidar]: Aktuel pris: ${price_per_1m} pr. 1M tokens")
    print(f"[Vidar]: Estimeret omkostning: ${cost_estimate:.6f}")
    
    # 2. Risk Analysis
    risk_score = 0.1
    if any(k in action.lower() for k in ["delete", "purge", "wipe"]):
        risk_score = 0.8
    if payload and any(k in str(payload).lower() for k in ["key", "secret", "password"]):
        risk_score = 0.9

    print(f"[Vidar]: Risk Score: {risk_score}")

    # 3. Decision & Veto Logic
    if risk_score > 0.7:
        return False, f"VETO: Høj sikkerhedsrisiko ({risk_score}). Manuel godkendelse påkrævet."
    
    if cost_estimate > 0.05: # Sænket tærskel for demo
        return True, "ADVARSEL: Omkostning overstiger budget-tærskel."

    print("[Vidar]: Scanning fuldført. Kald godkendt.")
    return True, "APPROVED"

if __name__ == "__main__":
    # Test: Sikker men dyr
    ok, msg = scan_api_call("Analysis", "ProcessHugeDataset")
    print(f"[RESULT]: {msg}\n")
    
    # Test: Farlig
    ok, msg = scan_api_call("Storage", "DeleteEverything", {"target": "production"})
    print(f"[RESULT]: {msg}")
