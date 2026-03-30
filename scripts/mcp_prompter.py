#!/usr/bin/env python3
"""
MCP Prompter v1.0
Fokus: Generering af system-prompter der instruerer agenter i at bruge MCP værktøjer.
Designet til at bygge bro mellem interne behov og eksterne handlinger.
"""
import os
import json

def generate_tool_prompt(need_summary, target_server):
    prompt = f"""# AGENT MISSION: EKSEKVERING AF HANDLING VIA MCP

## BAGGRUND:
Systemet har identificeret følgende behov: {need_summary}

## DIN OPGAVE:
Du skal interagere med MCP serveren '{target_server}' for at løse opgaven.

## INSTRUKTIONER:
1. Brug 'list_tools' til at se tilgængelige funktioner på '{target_server}'.
2. Identificer det mest relevante værktøj til at løse behovet.
3. Forespørg brugeren om bekræftelse (Accept Logik) før du udfører skrivende handlinger.
4. Dokumentér resultatet i data/episodes.jsonl.

Husk at overholde Yggdras principper om præcision og bruger-kontrol.
"""
    return prompt

if __name__ == "__main__":
    test_need = "Booke et opfølgningsmøde om V6 arkitektur"
    test_server = "google-calendar-mcp"
    print("--- MCP Prompter: Genereret System Prompt ---")
    print(generate_tool_prompt(test_need, test_server))
