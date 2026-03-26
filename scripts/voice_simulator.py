#!/usr/bin/env python3
"""
Voice Cadence Simulator v1.0
Tester "Thinking out loud"-princippet fra LIB.research/ai-frontier/topics/voice-cadence.md
"""
import time
import random

def thinking_out_loud_sim(user_query):
    # acknowledge hurtigt (The 300ms Rule)
    print(f"\n[USER]: {user_query}")
    time.sleep(0.3)
    
    acknowledgements = [
        "Lad mig se...",
        "Jeg tjekker lige biblioteket...",
        "Interessant, lad mig tænke...",
        "Det kigger jeg lige på..."
    ]
    
    print(f"[VOICE - ACK]: {random.choice(acknowledgements)}")
    
    # Simulerer LLM "deep thinking" latency
    print("[... Deep Thinking (LLM Processing) ...]")
    time.sleep(2.5)
    
    # Leverer svaret i korte bidder (chunks for hurtigere TTS start)
    response_chunks = [
        "Jeg har fundet 3 relevante kilder i LIB.research.",
        "Den vigtigste handler om agent-arkitekturer.",
        "Skal jeg opsummere den for dig?"
    ]
    
    for chunk in response_chunks:
        print(f"[VOICE - CHUNK]: {chunk}")
        time.sleep(0.8) # Simulerer TTS afspilnings-tid per chunk

if __name__ == "__main__":
    thinking_out_loud_sim("Hvad er status på min research om agenter?")
