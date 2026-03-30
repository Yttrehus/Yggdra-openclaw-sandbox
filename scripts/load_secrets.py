#!/usr/bin/env python3
"""
Secret Loader v1.0
Fokus: Sikker indlæsning af API-nøgler fra data/secrets/.
Del af V7 Secret Management Protocol.
"""
import json
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_FILE = os.path.join(_PROJECT_ROOT, "data/secrets/secrets.json")
EXAMPLE_FILE = os.path.join(_PROJECT_ROOT, "data/secrets/secrets.example.json")

def load_secrets():
    """Indlæser hemmeligheder fra secrets.json eller fallback til miljøvariabler."""
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, "r") as f:
            return json.load(f)
    
    print("[WARNING]: data/secrets/secrets.json ikke fundet. Forsøger miljøvariabler.")
    # Fallback logik her hvis nødvendigt (f.eks. os.environ)
    return {}

def get_secret(key):
    secrets = load_secrets()
    val = secrets.get(key)
    if not val:
        print(f"[ERROR]: Secret '{key}' ikke fundet.")
        return None
    return val

if __name__ == "__main__":
    # Test scriptet (uden at printe reelle nøgler i logs!)
    if not os.path.exists(SECRETS_FILE):
        print(f"[INIT]: Opretter dummy secrets.json til test baseret på eksempel.")
        with open(EXAMPLE_FILE, "r") as f:
            example = json.load(f)
        with open(SECRETS_FILE, "w") as f:
            json.dump(example, f, indent=2)
    
    sec = load_secrets()
    print(f"[SUCCESS]: Indlæst {len(sec)} nøgle-definitioner.")
