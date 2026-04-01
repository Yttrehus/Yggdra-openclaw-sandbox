#!/usr/bin/env python3
"""
Yggdra V7.2 Multi-Modal Demonstration
Fokus: End-to-end flow der kombinerer lokation, vejr, tid og rejse-logik.
"""
import time
import os
import json
from datetime import datetime, timezone

def run_multimodal_demo():
    print("================================================================")
    print("   YGGDRA V7.2: MULTI-MODAL CONTEXT DEMONSTRATION")
    print("================================================================\n")

    # 1. Lokations-detektering
    print("[TRIN 1]: Autonom Lokations-detektering...")
    os.system("python3 scripts/geo_location_v7.py")
    time.sleep(1)

    # 2. Timezone & Time of Day
    print("\n[TRIN 2]: Tids-synkronisering (Temporalt lag)...")
    os.system("python3 scripts/time_zone_v7.py")
    os.system("python3 scripts/time_of_day_v7.py")
    time.sleep(1)

    # 3. Vejr-kontekst
    print("\n[TRIN 3]: Miljø-bevidsthed (Meteorologisk lag)...")
    os.system("python3 scripts/weather_context.py")
    time.sleep(1)

    # 4. Travel Logic & Prediction
    print("\n[TRIN 4]: Rejse-logik & Forudsigelse (Mobilitets lag)...")
    # Simuler skift fra Aarhus for at trigger velkomst
    with open("data/travel_state.json", "w") as f:
        json.dump({"last_city": "Aarhus"}, f)
    os.system("python3 scripts/travel_logic_v7.py")
    os.system("python3 scripts/flight_aware_mock.py")
    time.sleep(1)

    # 5. Routine & Agenda
    print("\n[TRIN 5]: Dags-planlægning (Planlægnings lag)...")
    os.system("python3 scripts/agenda_vocalizer.py")
    os.system("python3 scripts/routine_engine_v7.py")
    time.sleep(1)

    # 6. Den Fuldendte Stemme
    print("\n[TRIN 6]: Den Proaktive Multi-Modale Hilsen...")
    os.system("python3 scripts/voice_simulator.py")

    print("\n================================================================")
    print("   DEMONSTRATION FULDENDT: MULTI-MODAL CONTEXT ER OPERATIONEL")
    print("================================================================")

if __name__ == "__main__":
    run_multimodal_demo()
