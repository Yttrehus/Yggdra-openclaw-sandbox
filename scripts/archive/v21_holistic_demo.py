#!/usr/bin/env python3
"""
Yggdra V21 Holistic Demonstration
Fokus: Den fulde emotionelle loop fra Vocal Sentiment Analysis til Empathic Voice Output.
Neural Empathy (V21)
"""
import os
import time
from v21_vocal_sentiment_poc import VocalSentimentAnalysis
from voice_emotional import get_emotional_tone

def run_v21_demo():
    print("================================================================")
    print("   YGGDRA V21: NEURAL EMPATHY - THE EMPATHIC PARTNER")
    print("================================================================\n")

    # 1. Vocal Sentiment Analysis (V21.1)
    print("[TRIN 1]: Analyserer vokal input for emotionelle nuancer...")
    analyzer = VocalSentimentAnalysis()
    # Simulerer frustreret input (fast kadence, høj pitch variation)
    mock_input = {"cadence": "fast", "pitch_variation": "high", "volume_spikes": True}
    sentiment = analyzer.analyze_vocal_input(mock_input)
    if sentiment:
        print(f"[SUCCESS]: Ejerens state identificeret som: '{sentiment['state']}'.")
    time.sleep(1)

    # 2. Emotional Tone Decision (V21.1 / voice_emotional)
    print("\n[TRIN 2]: Tilpasser assistentens emotionelle tone...")
    tone = get_emotional_tone(vocal_sentiment=sentiment)
    if tone:
        print(f"[SUCCESS]: Ny tone valgt: '{tone['tone'].upper()}'.")
        print(f"[DETAIL]: {tone['description']}")
    time.sleep(1)

    # 3. Voice Output Synthesis (V7.1 Simulation)
    print("\n[TRIN 3]: Syntetiserer empathic voice output...")
    print(f"[VOICE]: (Soft Tone, Pitch: {tone['pitch']}, Speed: {tone['speed']})")
    print("[VOICE]: Jeg kan mærke, at du har en travl dag. Skal jeg tage over på nogle af de rutine-opgaver?")

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: V21 EMPATI ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_v21_demo()
