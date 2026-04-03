#!/usr/bin/env python3
"""
Yggdra V8: Collaborative Intelligence Demo
Fokus: End-to-end flow med Multi-Agent koordinering, prissætning og sikkerheds-veto.
"""
import os
import time

def run_v8_demo():
    print("================================================================")
    print("   YGGDRA V8: COLLABORATIVE INTELLIGENCE DEMONSTRATION")
    print("================================================================\n")

    # 1. Multi-Agent Koordinering
    print("[TRIN 1]: Orkestrering af komplekst projekt (V7 Integration)...")
    os.system("python3 scripts/multi_agent_coordinator.py")
    time.sleep(1)

    # 2. Vidar Pricing Sync
    print("\n[TRIN 2]: Opdatering af realtids token-priser...")
    os.system("python3 scripts/vidar_pricing_sync.py")
    time.sleep(1)

    # 3. Decision Support & Security Scan (Normal)
    print("\n[TRIN 3]: Analyse af dagsorden og sikkerhedstjek (Godkendt)...")
    os.system("python3 scripts/execution_engine.py shift_focus_v6")
    time.sleep(1)

    # 4. Vidar Veto Simulation (Høj risiko)
    print("\n[TRIN 4]: Simulation af Veto ved farlig handling...")
    # Vi opretter et midlertidigt forslag i loggen til testen
    proposal = {
        "id": "danger_zone",
        "title": "Wipe All Cloud Secrets",
        "action": "scripts/wipe_secrets.sh --force",
        "reason": "Security protocol alpha"
    }
    with open("data/proposed_decisions.json", "w") as f:
        import json
        json.dump({"proposals": [proposal]}, f)
    
    os.system("python3 scripts/execution_engine.py danger_zone")
    time.sleep(1)

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: KOLLEKTIV INTELLIGENS ER AKTIV")
    print("================================================================")

if __name__ == "__main__":
    run_v8_demo()
