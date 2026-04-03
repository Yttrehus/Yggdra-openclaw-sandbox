#!/usr/bin/env python3
"""
Yggdra V22 Holistic Demonstration
Fokus: Den fulde kognitive synkroniserings-loop fra Flow-detektion til Predictive Intake.
Neural Convergence 2.0 (V22)
"""
import os
import time
from v22_cognitive_sync_poc import CognitiveSync
from v22_predictive_intake_poc import PredictiveIntake

def run_v22_demo():
    print("================================================================")
    print("   YGGDRA V22: NEURAL CONVERGENCE 2.0 - SYMBIOTIC FLOW")
    print("================================================================\n")

    # 1. Cognitive Sync (V22.1)
    print("[TRIN 1]: Monitorerer ejerens kognitive tilstand...")
    sync = CognitiveSync()
    mock_activity = {"typing_speed": "high", "active_apps": ["VS Code", "Terminal"], "context_switches": "low"}
    sync_state = sync.analyze_cognitive_load(mock_activity)
    if sync_state:
        print(f"[SUCCESS]: Kognitiv synkronisering opnået (State: {sync_state['state']}).")
    time.sleep(1)

    # 2. Predictive Intake (V22.2)
    print("\n[TRIN 2]: Forbereder næste opgaver baseret på kognitiv kontekst...")
    intake = PredictiveIntake()
    predictions = intake.predict_next_tasks()
    if predictions:
        print(f"[SUCCESS]: Næste opgaver forberedt proaktivt.")
    time.sleep(1)

    # 3. Kognitiv Symbiose (V22.3)
    print("\n[TRIN 3]: Integrerer prædiktioner i ejerens workflow...")
    print(f"[VOICE]: Jeg har detekteret at du er i et dybt flow med {mock_activity['active_apps'][0]}.")
    print(f"[VOICE]: Jeg har automatisk forberedt '{predictions[0]['task']}' som din næste handling.")
    print(f"[VOICE]: Skal jeg eksekvere den i baggrunden nu?")

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V22 SYMBIOSE ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v22_demo()
