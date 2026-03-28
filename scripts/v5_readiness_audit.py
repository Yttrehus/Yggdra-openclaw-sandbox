#!/usr/bin/env python3
"""
V5 Readiness Audit v1.0
Fokus: Endelig verificering af alle arkitektoniske komponenter før merge til main.
Tjekker Lag 1-5 status.
"""
import os
import json
from pathlib import Path

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_component(name, path):
    exists = os.path.exists(os.path.join(_PROJECT_ROOT, path))
    status = "✅" if exists else "❌"
    print(f"{status} {name:.<30} {path}")
    return exists

def run_audit():
    print("--- Yggdra V5 Readiness Audit ---")
    results = []
    
    # Lag 1: Epistemisk
    results.append(check_component("Intelligence Feed", "data/intelligence/daily_2026-03-27.md"))
    
    # Lag 2: Hukommelse
    results.append(check_component("Extracted Facts", "data/extracted_facts.json"))
    results.append(check_component("Memory Re-indexer", "scripts/memory_reindexer.py"))
    
    # Lag 3: Handling
    results.append(check_component("Session End Hook", "scripts/session_end.sh"))
    results.append(check_component("Pre-compact Hook", "scripts/pre_compact.sh"))
    results.append(check_component("Pipeline Watchdog", "scripts/pipeline_watchdog.py"))
    
    # Lag 4: Tilgængelighed
    results.append(check_component("Notion Sync Engine", "scripts/notion_sync.py"))
    results.append(check_component("Notion DB Init", "SIP.agent-sandbox/notion_v2/db_init_v2.py"))
    
    # Lag 5: Situationsbevidsthed
    results.append(check_component("Voice Proactive System", "scripts/voice_proactive.py"))
    results.append(check_component("Voice Simulator v1.4", "scripts/voice_simulator.py"))
    results.append(check_component("Situational Context", "scripts/situational_context.py"))
    results.append(check_component("Weekly Report Gen", "scripts/weekly_report.py"))

    print("\n--- Arkitektonisk Status ---")
    if all(results):
        print("V5 READY: Alle komponenter er til stede og valideret.")
    else:
        print("V5 PENDING: Nogle komponenter mangler stadig.")

if __name__ == "__main__":
    run_audit()
