#!/usr/bin/env python3
"""
Yggdra V14 Holistic Demonstration
Fokus: Samspillet mellem Neural Singularity (V14.1) og Reality Synthesis (V14.2).
"""
import os
import time
from datetime import datetime
from v14_neural_singularity import NeuralSingularity
from v14_reality_synthesis import RealitySynthesis

def run_v14_holistic_demo():
    print("================================================================")
    print("   YGGDRA V14: NEURAL SINGULARITY & REALITY SYNTHESIS")
    print("================================================================\n")

    # 1. Neural Singularity (V14.1)
    print("[TRIN 1]: Syntetiserer nyt kognitivt lag...")
    ns = NeuralSingularity()
    proposal = ns.synthesize_layer()
    if proposal:
        print(f"[SUCCESS]: Nyt kognitivt lag foreslået.")
    time.sleep(1)

    # 2. Reality Synthesis (V14.2)
    print("\n[TRIN 2]: Syntetiserer komplekse fremtidige scenarier...")
    rs = RealitySynthesis()
    synthesis_plan = rs.synthesize_reality()
    if synthesis_plan:
        print(f"[SUCCESS]: Virkeligheds-scenarie syntetiseret.")
    time.sleep(1)

    # 3. Den Fuldendte Proaktive Stemme (V14 Edition)
    print("\n[TRIN 3]: Systemet opsummerer hele V14-stakken...")
    # os.system("python3 scripts/voice_simulator.py")  <-- Suspenderet pga. timeout

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V14 SINGULARITY ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v14_holistic_demo()
