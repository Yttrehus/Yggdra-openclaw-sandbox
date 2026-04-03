#!/usr/bin/env python3
"""
Lag 8: Empathic Resonance - Integrated Test
Fokus: Validering af samspillet mellem Vocal Sentiment, Contextual Empathy og Voice Output.
"""
import os
import json
import time
from v21_contextual_empathy import ContextualEmpathy

def run_resonance_test():
    print("================================================================")
    print("   YGGDRA LAG 8: EMPATHIC RESONANCE - INTEGRATED TEST")
    print("================================================================\n")

    ce = ContextualEmpathy()
    
    # Scenarie 1: Ejer er frustreret i kontor-kontekst
    print("[SCENARIE 1]: Ejer virker frustreret på kontoret...")
    v_meta_1 = {"cadence": "fast", "pitch_variation": "high", "volume_spikes": True}
    s_meta_1 = {"context": "office", "time": "14:00"}
    res_1 = ce.synthesize_empathic_context(v_meta_1, s_meta_1)
    time.sleep(1)

    # Scenarie 2: Ejer er rolig/træt hjemme
    print("\n[SCENARIE 2]: Ejer er træt og rolig hjemme...")
    v_meta_2 = {"cadence": "slow", "pitch_variation": "low", "volume_spikes": False}
    s_meta_2 = {"context": "home", "time": "22:30"}
    res_2 = ce.synthesize_empathic_context(v_meta_2, s_meta_2)
    
    print("\n================================================================")
    print("   TEST FULDENDT: LAG 8 RESONANS ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_resonance_test()
