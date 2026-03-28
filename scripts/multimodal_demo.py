#!/usr/bin/env python3
"""
Multimodal Flow Demo v1.0
Fokus: Simulation af broen mellem Voice-start og Notion-check.
Del af Lag 4 (Tilgængelighed) og Lag 5 (Situationsbevidsthed).
"""
import time
import os
import json

def run_demo(user_input=None):
    print("--- Multimodal Flow Demo: Voice -> Notion ---")
    
    # 1. Voice Proactive Start (Simulation)
    print("\n[SCENE]: Ejeren sætter sig ind i bilen (Route 256).")
    time.sleep(1)
    print("[VOICE]: Godmorgen. Pipelinen kører perfekt. Din hukommelse er 87.3% pålidelig.")
    print("[VOICE]: Jeg bemærker du har 3 aktive projekter. Skal jeg sende status til din Notion?")
    
    # 2. Bruger accept (Simulation eller Input)
    if user_input is None:
        # Simuleret venten på input i terminal hvis ikke angivet
        print("\n[Venter på svar: 'ja' / 'nej' / 'senere']")
        return

    print(f"\n[USER]: {user_input}")
    
    # 3. Decision Logic (Lag 3 Handling)
    if user_input.lower() in ["ja", "gør det", "ok"]:
        print("\n[VOICE]: Modtaget. Synkroniserer nu...")
        os.system("python3 scripts/notion_sync.py --dry-run")
        print("\n[VOICE]: Done. Du kan nu se det opdaterede overblik på din telefon.")
        print("[SCENE]: Ejeren åbner Notion på sin mobil og ser de 3 projekter med Confidence-scores.")
    elif user_input.lower() in ["nej", "ikke nu"]:
        print("\n[VOICE]: Helt i orden. Jeg minder dig ikke om det igen i dag.")
    elif user_input.lower() in ["senere", "vent"]:
        print("\n[VOICE]: Modtaget. Jeg spørger igen om et par timer, når du er færdig med at køre.")
    else:
        print(f"\n[VOICE]: Jeg er ikke helt sikker på hvad du mente med '{user_input}'. Skal jeg synkronisere alligevel?")

if __name__ == "__main__":
    import sys
    user_choice = sys.argv[1] if len(sys.argv) > 1 else None
    run_demo(user_choice)
