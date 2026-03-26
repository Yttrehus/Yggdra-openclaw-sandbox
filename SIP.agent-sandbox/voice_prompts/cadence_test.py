import time
import sys

def simulate_voice_response(text):
    """
    Simulerer Voice Experience kadence principper (korte sætninger + thinking out loud).
    """
    sentences = text.split('. ')
    
    print("--- Simulation: Real-time Voice Cadence ---")
    print(f"Input: {text}\n")
    
    # Acknowledge hurtigt (The 300ms Rule simulation)
    print("[TTS START] Lad mig se...")
    time.sleep(0.3)
    
    for i, s in enumerate(sentences):
        # Fjern punktum hvis det findes
        clean_s = s.strip().rstrip('.')
        print(f"[TTS CHUNK {i+1}] {clean_s}.")
        # Simuler TTS afspilningstid baseret på ordlængde
        delay = len(clean_s.split()) * 0.4
        time.sleep(delay)

if __name__ == "__main__":
    test_text = "Vi er færdige med at designe Notion synkroniseringen. Den bruger nu REST API'et direkte. Jeg mangler kun din API nøgle for at initialisere databasen."
    simulate_voice_response(test_text)
