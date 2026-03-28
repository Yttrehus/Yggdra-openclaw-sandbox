import os
import sys
import time
import random
import json
import glob
import re
from datetime import datetime, timezone
import voice_proactive

# Pathing
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
REPORT_DIR = os.path.join(_PROJECT_ROOT, "memory/weekly_reports")

def load_facts():
    if os.path.exists(FACTS_FILE):
        try:
            with open(FACTS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading facts: {e}")
    return []

def load_latest_report():
    reports = glob.glob(os.path.join(REPORT_DIR, "*.md"))
    if not reports:
        return None
    latest_report = max(reports, key=os.path.getctime)
    with open(latest_report, "r") as f:
        return f.read()

def parse_report_to_chunks(report_content):
    chunks = []
    lines = report_content.split('\n')
    title = lines[0].replace('# ', '').strip()
    chunks.append(f"Her er {title}.")
    
    current_section = ""
    for line in lines[1:]:
        if line.startswith('## '):
            current_section = line.replace('## ', '').strip()
            if "Læringer" in current_section:
                chunks.append("Jeg har opsummeret ugens læringer.")
        elif line.startswith('- ') and "Læringer" in current_section:
            # Rens markdown og stjerner for tale
            fact = line.replace('- ', '').strip()
            fact = fact.split(' *(Kilde:')[0].strip() # Fjern kilde metadata
            fact = fact.replace('⭐', '') # Fjern stjerner fra tale-output
            chunks.append(fact)
            if len(chunks) > 6: # Begræns antal chunks for voice brevity
                break
    
    chunks.append("Det var ugens overblik. Skal jeg gå i dybden med noget?")
    return chunks

def format_relative_time(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = now - dt
        
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        
        if days == 0:
            if hours == 0:
                return "for nylig"
            elif hours == 1:
                return "for en time siden"
            else:
                return f"for {hours} timer siden"
        elif days == 1:
            return "i går"
        elif days < 7:
            return f"for {days} dage siden"
        else:
            return f"for {days // 7} uger siden"
    except Exception:
        return "tidligere"

def get_fact_chunks(query):
    # Tjek om brugeren beder om system status / sundhed
    if any(keyword in query.lower() for keyword in ["status", "sundhed", "fejl", "audit"]):
        report_path = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                content = f.read()
            issues = [line.strip("- ") for line in content.split('\n') if "[CRITICAL]" in line or "[HIGH]" in line]
            if issues:
                return ["Jeg har fundet kritiske fejl i pipelinen.", f"Der er {len(issues)} advarsler lige nu."] + issues[:2] + ["Du bør tjekke recovery guiden."]
            else:
                return ["Systemet kører optimalt.", "Alle fødekæder er grønne."]
        else:
            return ["Jeg kan ikke finde den seneste audit rapport."]

    # Tjek om brugeren beder om en rapport
    if any(keyword in query.lower() for keyword in ["rapport", "overblik", "uge", "resume"]):
        report = load_latest_report()
        if report:
            return parse_report_to_chunks(report)
        else:
            return ["Jeg kunne ikke finde en ugerapport.", "Du kan køre scripts/weekly_report.py for at generere en."]

    facts = load_facts()
    if not facts:
        return ["Jeg kunne ikke indlæse fakta fra databasen.", "Tjek venligst data/extracted_facts.json."]
    
    keywords = query.lower().split()
    relevant = []
    for f in facts:
        if any(k in f['fact'].lower() for k in keywords):
            relevant.append(f)
    
    if not relevant:
        relevant = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]
        prefix = "Jeg fandt ikke specifikke matches, men her er det nyeste fra min hukommelse:"
    else:
        prefix = f"Jeg har fundet {len(relevant)} relevante fakta om det emne."

    chunks = [prefix]
    for r in relevant[:3]:
        time_context = format_relative_time(r.get('timestamp', ''))
        chunks.append(f"{r['fact']} (lært {time_context}).")
    
    chunks.append("Skal jeg dykke dybere ned i nogle af dem?")
    return chunks

def thinking_out_loud_sim(user_query=None):
    if user_query is None:
        print(f"\n--- Yggdra Voice Session Start ---")
        greeting = voice_proactive.generate_greeting()
        chunks = re.split(r'\. ', greeting)
        for chunk in chunks:
            if chunk.strip():
                print(f"[VOICE - PROACTIVE]: {chunk.strip().rstrip('.')}.")
                time.sleep(1.2)
        return

    print(f"\n[USER]: {user_query}")
    time.sleep(0.3)
    
    acknowledgements = [
        "Lad mig tjekke min hukommelse...",
        "Jeg kigger lige i de udtrukne fakta...",
        "Et øjeblik, jeg henter data...",
        "Lad mig se hvad jeg ved om det..."
    ]
    
    if any(keyword in user_query.lower() for keyword in ["rapport", "overblik", "uge", "resume"]):
        print("[VOICE - ACK]: Jeg henter ugens overblik til dig...")
    else:
        print(f"[VOICE - ACK]: {random.choice(acknowledgements)}")
    
    print("[... Deep Thinking (LLM & Fact Retrieval) ...]")
    time.sleep(1.2)
    
    response_chunks = get_fact_chunks(user_query)
    
    for chunk in response_chunks:
        # Rens for stjerner i alle chunks
        clean_chunk = chunk.replace('⭐', '')
        print(f"[VOICE - CHUNK]: {clean_chunk}")
        delay = len(clean_chunk.split()) * 0.25 + 0.5
        time.sleep(delay)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        thinking_out_loud_sim(query)
    else:
        thinking_out_loud_sim(None)
