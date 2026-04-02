#!/usr/bin/env python3
"""
Yggdra V10 Holistic Demonstration
Fokus: Samspillet mellem Neural Synthesis (V10.1) og Autonomous Goal Drills (V10.2).
"""
import os
import time
from datetime import datetime
from v10_neural_synthesis import NeuralSynthesis
from v10_autonomous_goal_drill import AutonomousGoalDrill

def run_v10_holistic_demo():
    print("================================================================")
    print("   YGGDRA V10: NEURAL SYNTHESIS & AUTONOMOUS GOAL DRILLS")
    print("================================================================\n")

    # 1. Neural Synthesis (V10.1)
    print("[TRIN 1]: Syntetiserer ny indsigt baseret på historiske episoder...")
    ns = NeuralSynthesis()
    insight = ns.synthesize_knowledge()
    if insight:
        print(f"[SUCCESS]: Ny indsigt genereret: {insight['fact']}")
    time.sleep(1)

    # 2. Autonomous Goal Drill (V10.2)
    print("\n[TRIN 2]: Gennemfører mål-øvelse baseret på de strategiske mål...")
    agd = AutonomousGoalDrill()
    drill_result = agd.run_drill()
    if drill_result:
        print(f"[SUCCESS]: Mål-øvelse gennemført med konsensus.")
    time.sleep(1)

    # 3. Den Fuldendte Proaktive Stemme (V10 Edition)
    print("\n[TRIN 3]: Systemet opsummerer hele V10-stakken...")
    # os.system("python3 scripts/voice_simulator.py")  <-- Suspenderet i denne demo

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V10 AUTONOMI ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v10_holistic_demo()
