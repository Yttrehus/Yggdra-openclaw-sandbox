#!/usr/bin/env python3
"""
Merge Translator v1.0
Hjælper med at mappe filer fra den gamle projects/ struktur til den nye flade struktur.
Bruges ved merge-konflikter mellem upstream/main og feature/v5-ready.
"""
import os
import shutil

MAPPING = {
    "projects/2_research/": "LIB.research/",
    "projects/REF.prompt-skabeloner/": "REF.prompt-skabeloner/",
    "projects/0_backlog/": "0_backlog/",
    "projects/BMS.auto-chatlog/": "BMS.auto-chatlog/",
    "projects/SIP.agent-sandbox/": "SIP.agent-sandbox/",
    "projects/DLR.context-engineering/": "DLR.context-engineering/"
}

def translate_structure():
    print("--- Structure Translation Tool ---")
    for old_prefix, new_prefix in MAPPING.items():
        if os.path.exists(old_prefix):
            print(f"Flytter indhold fra {old_prefix} til {new_prefix}...")
            if not os.path.exists(new_prefix):
                os.makedirs(new_prefix)
            
            for item in os.listdir(old_prefix):
                old_path = os.path.join(old_prefix, item)
                new_path = os.path.join(new_prefix, item)
                
                if os.path.exists(new_path):
                    print(f"  [SKIP] {item} findes allerede i destinationen.")
                else:
                    shutil.move(old_path, new_path)
                    print(f"  [MOVE] {item}")
            
            # Fjern den gamle mappe hvis den er tom
            try:
                os.removedirs(old_prefix)
                print(f"  [CLEAN] Fjernede tom mappe: {old_prefix}")
            except OSError:
                pass

if __name__ == "__main__":
    translate_structure()
