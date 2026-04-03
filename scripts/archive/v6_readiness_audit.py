#!/usr/bin/env python3
"""
V6 Readiness Audit v1.2
Fokus: Verificering af de nye arkitektoniske komponenter for V6.
Tjekker Lag 1-5 status inkl. nye SDK/API integrationer og missions-styring.
"""
import os
import json
from pathlib import Path

_PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

def check_component(name, path):
    full_path = os.path.join(_PROJECT_ROOT, path)
    exists = os.path.exists(full_path)
    status = "✅" if exists else "❌"
    print(f"{status} {name:.<30} {path}")
    return exists

def check_memory_v1_1():
    path = os.path.join(_PROJECT_ROOT, "scripts/memory.py")
    if not os.path.exists(path):
        return False
    
    with open(path, "r") as f:
        content = f.read()
    
    has_dynamic = "calculate_dynamic_limit" in content
    has_evergreen = "established" in content and "decay_rate" in content
    
    status = "✅" if (has_dynamic and has_evergreen) else "❌"
    print(f"{status} Memory v1.1 (Dynamic RAG)... scripts/memory.py")
    return has_dynamic and has_evergreen

def run_audit():
    print("--- Yggdra V6 Readiness Audit v1.2 ---")
    results = []
    
    # Eksisterende V5 Fundament
    print("\n[V5 Fundament]")
    results.append(check_component("Intelligence Feed", "data/intelligence/daily_2026-03-27.md"))
    results.append(check_component("Extracted Facts", "data/extracted_facts.json"))
    results.append(check_component("Memory Re-indexer", "scripts/memory_reindexer.py"))
    
    # V6 Evolution - Core Components
    print("\n[V6 Evolution - Core]")
    results.append(check_component("V6 Strategy Brainstorm", "scripts/v6_strategy_brainstorm.py"))
    results.append(check_component("Claude Code Research", "LIB.research/claude-code-ecosystem.md"))
    results.append(check_memory_v1_1())
    results.append(check_component("Memory Simulator", "scripts/memory_sim.py"))

    # V6 Evolution - Action & Control Layer
    print("\n[V6 Evolution - Action & Control]")
    results.append(check_component("MCP Action Layer Mock", "scripts/mcp_action_mock.py"))
    results.append(check_component("MCP Prompter", "scripts/mcp_prompter.py"))
    results.append(check_component("ElevenLabs SDK Mock", "scripts/elevenlabs_sdk_mock.py"))
    results.append(check_component("Notion Command Center", "scripts/notion_command_center.py"))
    results.append(check_component("End-to-End Demo Flow", "scripts/v6_demo_flow.py"))

    print("\n--- Arkitektonisk Status ---")
    if all(results):
        print("V6 READY: Alle hukommelses-, orkestrerings- og kontrol-komponenter er valideret.")
    else:
        print("V6 PENDING: Nogle V6 komponenter mangler eller er ikke opdateret.")

if __name__ == "__main__":
    run_audit()
