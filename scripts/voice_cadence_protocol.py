#!/usr/bin/env python3
"""
Voice Cadence Protocol v1.0
Fokus: Optimering af talestrøm (pauser, hastighed) baseret på informationstæthed.
Del af Lag 5 (Situationsbevidsthed) / V6.4 Oplevelses-evolution.
"""
import time
import re

def speak_with_cadence(text, base_delay=1.0):
    """Simulerer tale med naturlige pauser baseret på tegnsætning."""
    # Definer pauser for forskellige tegn
    pauses = {
        r'\.': 1.5,  # Punktum: Lang pause
        r'\?': 1.6,  # Spørgsmålstegn: Ekstra lang pause til refleksion
        r'\!': 1.2,  # Udråbstegn: Kontant pause
        r',': 0.6,   # Komma: Kort pause
        r':': 0.8,   # Kolon: Forventningsfuld pause
    }
    
    print("--- Starting Voice Output with Cadence Protocol ---")
    
    # Split tekst i bidder baseret på tegnsætning, men behold tegnene
    chunks = re.split(r'([.,?!:])', text)
    
    for i in range(0, len(chunks)-1, 2):
        sentence_part = chunks[i].strip()
        punctuation = chunks[i+1]
        
        if sentence_part:
            full_segment = sentence_part + punctuation
            print(f"[VOICE]: {full_segment}")
            
            # Find den relevante pause
            delay = pauses.get(f"\\{punctuation}", base_delay)
            time.sleep(delay)
            
    # Håndter eventuel resterende tekst uden slut-tegn
    if len(chunks) % 2 != 0 and chunks[-1].strip():
        print(f"[VOICE]: {chunks[-1].strip()}.")

if __name__ == "__main__":
    sample_text = "Jeg har analyseret din hukommelse. Vi er nu 29 procent i mål, hvilket er en god start. Men, er du klar til at intensivere arbejdet? Der er nemlig opstået en fejl i pipelinen!"
    speak_with_cadence(sample_text)
