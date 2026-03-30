#!/usr/bin/env python3
"""
Execution Trigger Mock v1.0
Fokus: Simulation af bruger-accept der trigger Execution Engine.
Del af V6.3 Kognitiv Guidance.
"""
import sys
import os
import execution_engine

def simulate_user_accept(decision_id):
    print(f"--- Voice Command Simulation: 'Ja, gør det' (for {decision_id}) ---")
    success = execution_engine.execute_decision(decision_id)
    if success:
        print(f"[TRIGGER]: Beslutning {decision_id} er nu under udførelse.")
    else:
        print(f"[TRIGGER]: Fejl ved eksekvering af {decision_id}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        simulate_user_accept(sys.argv[1])
    else:
        # Standard: Sprint intensivering
        simulate_user_accept("shift_focus_v6")
