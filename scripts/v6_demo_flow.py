#!/usr/bin/env python3
"""
V6 End-to-End Demo Flow v1.1
Fokus: Simulation af den fulde arkitektoniske kæde inkl. GPS skift.
"""
import time
import os

def run_v6_demo():
    print("--- Yggdra V6 End-to-End Flow Demonstration ---")
    
    # 1. Geografisk event (Simulation)
    print("\n[STEP 1]: Brugeren ankommer til kontoret...")
    os.system("python3 scripts/gps_trigger_mock.py office")
    time.sleep(1)

    # 2. Start med Voice Proactive (Lag 5)
    print("\n[STEP 2]: Systemet vågner og tilpasser sig lokationen...")
    os.system("python3 scripts/voice_simulator.py")
    
    # 3. Discovery logik (Lag 3)
    print("\n[STEP 3]: Hugin & Ratatosk analyserer behov...")
    os.system("python3 scripts/multi_agent_mock.py")
    
    # 4. Handling: Generate Mission (Lag 3)
    print("\n[STEP 4]: Genererer Missions-brief til handling...")
    os.system("python3 scripts/mcp_prompter.py")
    
    # 5. Notion Push: Command Center (Lag 4)
    print("\n[STEP 5]: Pusher mission til Notion Command Center...")
    os.system("python3 scripts/notion_command_center.py")
    
    print("\n[DEMO COMPLETE]: Yggdra V6 er nu fuldt integreret med tid, rum og handling.")
    print("Systemet har automatisk skiftet til 'office' mode og forberedt de relevante værktøjer.")

if __name__ == "__main__":
    run_v6_demo()
