import os
import sys
import time
import random
import json
import glob
import re
from datetime import datetime, timezone
import voice_proactive
import voice_emotional

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

def calculate_dynamic_limit(query):
    """Beregner limit baseret på forespørgslens kompleksitet (fra memory.py v1.1)."""
    words = len(query.split())
    if words < 3: return 5
    if words < 8: return 10
    return 20

def get_fact_chunks(query):
    # Check if user asks specifically for status/health
    if any(keyword in query.lower() for keyword in ["status", "sundhed", "fejl", "audit"]):
        if len(query.split()) < 4:
            report_path = os.path.join(_PROJECT_ROOT, "data/maintenance_report.md")
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    content = f.read()
                issues = [line.strip("- ") for line in content.split('\n') if "[CRITICAL]" in line or "[HIGH]" in line]
                if issues:
                    return ["Jeg har fundet kritiske fejl i pipelinen.", f"Der er {len(issues)} advarsler lige nu."] + issues[:2] + ["Du bør tjekke recovery guiden."]
                else:
                    return ["Systemet kører optimalt.", "Alle fødekæder er grønne."]

    # Tjek om brugeren beder om en rapport
    if any(keyword in query.lower() for keyword in ["rapport", "overblik", "uge", "resume"]):
        report = load_latest_report()
        if report:
            return parse_report_to_chunks(report)

    facts = load_facts()
    if not facts:
        return ["Jeg kunne ikke indlæse fakta fra databasen."]
    
    limit = calculate_dynamic_limit(query)
    query_words = set(re.findall(r'\w+', query.lower()))
    relevant = []
    for f in facts:
        fact_words = set(re.findall(r'\w+', f['fact'].lower()))
        if query_words.intersection(fact_words):
            relevant.append(f)
    
    if not relevant:
        relevant = sorted(facts, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]
        prefix = "Jeg fandt ikke specifikke matches, men her er det nyeste fra min hukommelse:"
    else:
        prefix = f"Jeg har fundet {len(relevant)} relevante fakta. Her er de {min(limit, len(relevant))} vigtigste:"

    chunks = [prefix]
    for r in relevant[:limit]:
        time_context = format_relative_time(r.get('timestamp', ''))
        chunks.append(f"{r['fact']} (lært {time_context}).")
    
    chunks.append("Skal jeg dykke dybere ned i nogle af dem?")
    return chunks

import os
import sys
import time
import random
import json
import glob
import re
from datetime import datetime, timezone
import voice_proactive
import voice_emotional
import episode_search
import goal_tracker

# Pathing
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
REPORT_DIR = os.path.join(_PROJECT_ROOT, "memory/weekly_reports")
DRIFT_STATUS_FILE = os.path.join(_PROJECT_ROOT, "data/drift_status.json")

def get_historical_context():
    """Henter de seneste episoder for at give narrativ kontinuitet."""
    try:
        episodes = episode_search.search_episodes("session_end")
        if not episodes:
            return ""
        
        last_episode = episodes[-1]
        ts = last_episode.get('timestamp', '')
        if ts:
            rel_time = "sidst" # Forenklet for demo
            return f"Siden vi sidst afsluttede en session {rel_time}, har jeg holdt øje med dine prioriteter. "
    except:
        pass
    return ""

def get_goal_summary():
    """Henter de seneste strategiske mål for at give strategisk fokus."""
    try:
        goals = goal_tracker.load_goals()
        if not goals:
            return ""
        
        main_goal = goals[0] # Antager første mål er vigtigst
        return f"Vi er nu {main_goal['progress']}% i mål med {main_goal['title']}. "
    except:
        pass
    return ""

def get_drift_warning():
    """Tjekker om der er en advarsel om drift (forældet backlog)."""
    try:
        if os.path.exists(DRIFT_STATUS_FILE):
            with open(DRIFT_STATUS_FILE, "r") as f:
                data = json.load(f)
                if "DRIFT DETECTED" in data.get("status", ""):
                    return f"Vigtig oplysning: {data['status']} "
    except:
        pass
    return ""

def thinking_out_loud_sim(user_query=None):
    # Hent emotionel profil
    tone = voice_emotional.get_emotional_tone()
    
    if user_query is None:
        print(f"\n--- Yggdra Voice Session Start (Tone: {tone['tone'].upper()}) ---")
        
        # 1. Hent historisk, strategisk og sundhedsmæssig kontekst (V6.1)
        history = get_historical_context()
        goals = get_goal_summary()
        drift = get_drift_warning()
        
        # 2. Generer proaktiv hilsen
        greeting = voice_proactive.generate_greeting()
        
        full_intro = history + goals + drift + greeting
        
        chunks = re.split(r'\. ', full_intro)
        for chunk in chunks:
            if chunk.strip():
                print(f"[VOICE - PROACTIVE]: {chunk.strip().rstrip('.')}.")
                # Juster delay baseret på hastighed
                delay = 0.8 if tone['speed'] == "faster" else 1.2
                time.sleep(delay)
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
    
    # Dynamic RAG feedback (V6)
    limit = calculate_dynamic_limit(user_query)
    if limit > 10:
        print(f"[VOICE - INTERNAL]: Kompleks forespørgsel detekteret. Udvidet retrieval aktiv.")

    print(f"[VOICE - INTERNAL]: Emotionel profil: {tone['description']}")
    time.sleep(1.0)
    
    response_chunks = get_fact_chunks(user_query)
    
    for chunk in response_chunks:
        clean_chunk = chunk.replace('⭐', '')
        print(f"[VOICE - CHUNK]: {clean_chunk}")
        # Juster formidlings-delay baseret på hastighed
        base_delay = len(clean_chunk.split()) * 0.25 + 0.5
        actual_delay = base_delay * 0.7 if tone['speed'] == "faster" else base_delay
        time.sleep(actual_delay)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        thinking_out_loud_sim(query)
    else:
        thinking_out_loud_sim(None)
