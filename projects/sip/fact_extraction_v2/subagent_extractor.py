import json
import os
import sys

# Simulation af subagent-baseret fact extraction (Gap 6)
# I et rigtigt OpenClaw miljø ville denne script kalde sessions_spawn

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
DIGEST_PATH = os.path.join(PROJECT_ROOT, "projects/auto-chatlog/sections-digest.json")

def simulate_subagent_extraction(text):
    """
    Simulerer en subagent turn der modtager rå tekst og returnerer strukturerede fakta.
    Her bruger vi blot en placeholder, da vi ikke kan kalde værktøjer direkte fra et python script
    uden for agent-loopet uden at bryde 'thinking' workflowet.
    """
    # Placeholder til når vi kalder denne fra agentens turn
    return []

def prepare_subagent_prompt(text):
    prompt = f"""
Du er en Fact Extraction Subagent. Din opgave er at læse nedenstående tekst og identificere atomiske fakta, beslutninger eller handlinger.
Returnér kun en JSON liste med objekter i dette format:
{{
  "fact": "Kort beskrivelse af faktum",
  "category": "work|action|research|meta|activity",
  "confidence": 0.0-1.0
}}

Tekst:
{text}
"""
    return prompt

if __name__ == "__main__":
    if not os.path.exists(DIGEST_PATH):
        print("Digest findes ikke.")
        sys.exit(1)
        
    with open(DIGEST_PATH, 'r') as f:
        digest = json.load(f)
        
    for section in digest.get('sections', []):
        combined_text = " ".join(section.get('userSamples', []) + section.get('assistantSamples', []))
        print(f"--- PROMPT TIL SUBAGENT (SEKTION {section['id']}) ---")
        print(prepare_subagent_prompt(combined_text[:500] + "..."))
        print("-" * 50)
