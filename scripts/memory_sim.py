#!/usr/bin/env python3
"""
Dynamic RAG & Temporal Decay Simulator v1.0
Simulerer logikken i scripts/memory.py v1.1 uden API-kald.
"""
import math
from datetime import datetime, timedelta

def calculate_dynamic_limit(query):
    words = len(query.split())
    if words < 3: return 5
    if words < 8: return 10
    return 20

def simulate_decay(age_days, confidence, base_rate=0.005):
    # Evergreen protection: 'established' viden decay'er langsommere
    current_decay_rate = base_rate
    if confidence == "established":
        current_decay_rate *= 0.1
        
    decay = 1 / (1 + math.log1p(age_days) * current_decay_rate * 10)
    return decay

def run_simulation():
    queries = [
        "AI status", 
        "Hvordan fungerer agent-arkitekturer?", 
        "En dybdegående analyse af Model Context Protocol og fremtidens API integrationer i autonome systemer"
    ]
    
    print("--- Dynamic RAG: Limit Simulation ---")
    for q in queries:
        limit = calculate_dynamic_limit(q)
        print(f"Query: '{q[:40]}...' -> Limit: {limit}")
        
    print("\n--- Temporal Decay: Score Simulation ---")
    scenarios = [
        {"age": 1, "conf": "research", "label": "Ny research"},
        {"age": 30, "conf": "research", "label": "Måned gammel research"},
        {"age": 30, "conf": "established", "label": "Måned gammel core-viden"},
        {"age": 365, "conf": "established", "label": "År gammel core-viden"},
        {"age": 365, "conf": "draft", "label": "År gammelt udkast"}
    ]
    
    for s in scenarios:
        score = simulate_decay(s['age'], s['conf'])
        print(f"Scenario: {s['label']:<25} | Alder: {s['age']:>3}d | Score: {score:.4f}")

if __name__ == "__main__":
    run_simulation()
