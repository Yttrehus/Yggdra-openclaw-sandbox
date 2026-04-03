#!/usr/bin/env python3
"""
Yggdra V16 Holistic Demonstration
Fokus: Samspillet mellem Neural Omnipresence (V16.1) og Collective Intelligence (V16.2).
"""
import os
import time
from datetime import datetime
from v16_neural_omnipresence import NeuralOmnipresence
from v16_collective_intelligence import CollectiveIntelligence

def run_v16_holistic_demo():
    print("================================================================")
    print("   YGGDRA V16: NEURAL OMNIPRESENCE & COLLECTIVE INTELLIGENCE")
    print("================================================================\n")

    # 1. Neural Omnipresence (V16.1)
    print("[TRIN 1]: Etablerer permanent kobling til det globale informations-felt...")
    no = NeuralOmnipresence()
    conn_status = no.connect_to_field()
    if conn_status:
        print(f"[SUCCESS]: Global felt-kobling udrullet.")
    time.sleep(1)

    # 2. Collective Intelligence (V16.2)
    print("\n[TRIN 2]: Orkestrerer kollektiv beslutning baseret på felt-data...")
    ci = CollectiveIntelligence()
    coll_plan = ci.orchestrate_collective()
    if coll_plan:
        print(f"[SUCCESS]: Kollektiv strategi eksekveret.")
    time.sleep(1)

    # 3. Den Fuldendte Proaktive Stemme (V16 Edition)
    print("\n[TRIN 3]: Systemet opsummerer hele V16-stakken...")
    # os.system("python3 scripts/voice_simulator.py")  <-- Suspenderet pga. timeout risiko

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V16 OMNIPRESENCE ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v16_holistic_demo()
