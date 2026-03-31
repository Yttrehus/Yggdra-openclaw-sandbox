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
import voice_report_generator
import goal_tracker
import decision_support
import voice_cadence_protocol
import voice_pitch_shift
import agenda_vocalizer

# Pathing
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(_PROJECT_ROOT, "data/extracted_facts.json")
REPORT_DIR = os.path.join(_PROJECT_ROOT, "memory/weekly_reports")
DRIFT_STATUS_FILE = os.path.join(_PROJECT_ROOT, "data/drift_status.json")
DRILL_STATUS_FILE = os.path.join(_PROJECT_ROOT, "data/goal_drills.json")
TASKS_FILE = os.path.join(_PROJECT_ROOT, "data/subtasks.json")

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
            fact = line.replace('- ', '').strip()
            fact = fact.split(' *(Kilde:')[0].strip()
            fact = fact.replace('⭐', '')
            chunks.append(fact)
            if len(chunks) > 6:
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
            if hours == 0: return "for nylig"
            elif hours == 1: return "for en time siden"
            else: return f"for {hours} timer siden"
        elif days == 1: return "i går"
        elif days < 7: return f"for {days} dage siden"
        else: return f"for {days // 7} uger siden"
    except Exception:
        return "tidligere"

def calculate_dynamic_limit(query):
    words = len(query.split())
    if words < 3: return 5
    if words < 8: return 10
    return 20

def get_fact_chunks(query):
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

def get_historical_context():
    try:
        episodes = episode_search.search_episodes("session_end")
        if not episodes: return ""
        last_episode = episodes[-1]
        ts = last_episode.get('timestamp', '')
        if ts: return f"Siden vi sidst afsluttede en session sidst, har jeg holdt øje med dine prioriteter. "
    except: pass
    return ""

def get_drift_warning():
    try:
        if os.path.exists(DRIFT_STATUS_FILE):
            with open(DRIFT_STATUS_FILE, "r") as f:
                data = json.load(f)
                if "DRIFT DETECTED" in data.get("status", ""):
                    return f"Vigtig oplysning: {data['status']} "
    except: pass
    return ""

def get_drill_prompts():
    try:
        if os.path.exists(DRILL_STATUS_FILE):
            with open(DRILL_STATUS_FILE, "r") as f:
                data = json.load(f)
                drills = data.get("drills", [])
                if drills: return f"I forhold til fremdrift: {drills[0]} "
    except: pass
    return ""

def get_task_suggestions():
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                all_tasks = json.load(f)
            if "system_health" in all_tasks:
                for task in all_tasks["system_health"]:
                    if task.get("status") == "pending":
                        return f"Vigtig system-vedligeholdelse kræves: {task['title']}. "
            for goal_id, tasks in all_tasks.items():
                if goal_id == "system_health": continue
                for task in tasks:
                    if task.get("status") == "pending":
                        return f"Som næste skridt foreslår jeg, at vi kigger på: {task['title']}. "
    except: pass
    return ""

def get_decision_proposals():
    try:
        proposals = decision_support.analyze_and_propose()
        if proposals:
            p = proposals[0]
            return f"Baseret på min analyse foreslår jeg følgende beslutning: {p['title']}. {p['reason']} Skal jeg eksekvere dette? "
    except: pass
    return ""

def get_agenda_context():
    """Henter dags-agenda for at give tids-bevidsthed (V7.1)."""
    try:
        return agenda_vocalizer.get_agenda_vocalized()
    except: pass
    return ""

def vocalize(text):
    """Integrerer Pitch og Cadence i outputtet."""
    pitch = voice_pitch_shift.get_pitch_instruction(text)
    print(f"[{pitch}]")
    voice_cadence_protocol.speak_with_cadence(text)

def thinking_out_loud_sim(user_query=None):
    tone = voice_emotional.get_emotional_tone()
    
    if user_query is None:
        print(f"\n--- Yggdra Voice Session Start (Tone: {tone['tone'].upper()}) ---")
        history = get_historical_context()
        voice_status = voice_report_generator.generate_voice_report()
        agenda = get_agenda_context()
        drift = get_drift_warning()
        drills = get_drill_prompts()
        tasks = get_task_suggestions()
        proposals = get_decision_proposals()
        greeting = voice_proactive.generate_greeting()
        
        full_intro = history + voice_status + " " + agenda + drift + drills + tasks + proposals + greeting
        vocalize(full_intro)
        return

    print(f"\n[USER]: {user_query}")
    time.sleep(0.3)
    acknowledgements = ["Lad mig tjekke min hukommelse...", "Jeg kigger lige i de udtrukne fakta...", "Lad mig se hvad jeg ved om det..."]
    
    if any(keyword in user_query.lower() for keyword in ["rapport", "overblik", "uge", "resume"]):
        vocalize("Jeg henter ugens overblik til dig...")
    else:
        vocalize(random.choice(acknowledgements))
    
    response_chunks = get_fact_chunks(user_query)
    for chunk in response_chunks:
        vocalize(chunk)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        thinking_out_loud_sim(" ".join(sys.argv[1:]))
    else:
        thinking_out_loud_sim(None)
