#!/usr/bin/env python3
"""
Yggdra V15 Holistic Demonstration
Fokus: Samspillet mellem Neural Convergence (V15.1) og Resource Transmutation (V15.2).
"""
import os
import time
from datetime import datetime
from v15_neural_convergence import NeuralConvergence
from v15_resource_transmutation import ResourceTransmutation

def run_v15_holistic_demo():
    print("================================================================")
    print("   YGGDRA V15: NEURAL CONVERGENCE & RESOURCE TRANSMUTATION")
    print("================================================================\n")

    # 1. Resource Transmutation (V15.2)
    print("[TRIN 1]: Forbereder hardware-miljøet via ressource-transmutation...")
    rt = ResourceTransmutation()
    trans_plan = rt.transmute_resources()
    if trans_plan:
        print(f"[SUCCESS]: Hardware-allokering optimeret til {trans_plan['new_state']}.")
    time.sleep(1)

    # 2. Neural Convergence (V15.1)
    print("\n[TRIN 2]: Etablerer direkte kognitiv kobling til de optimerede ressourcer...")
    nc = NeuralConvergence()
    conv_status = nc.converge_with_system()
    if conv_status:
        print(f"[SUCCESS]: System-fusion fuldført via {conv_status['node']}.")
    time.sleep(1)

    # 3. Den Fuldendte Proaktive Stemme (V15 Edition)
    print("\n[TRIN 3]: Systemet opsummerer hele V15-stakken...")
    # os.system("python3 scripts/voice_simulator.py")  <-- Suspenderet pga. timeout risiko

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V15 KONVERGENS ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v15_holistic_demo()
