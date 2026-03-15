# Autonomous AI Setup — Praktisk Research

> Udført 2026-02-22. Fokus: hvad andre gør, og hvad vi konkret kan adoptere.

---

## 1. Hvad Andre Gør (Der Virker)

### 1.1 Daniel Miessler — Personal AI Infrastructure (PAI)

**Repo:** https://github.com/danielmiessler/Personal_AI_Infrastructure

Miessler har bygget PAI oven på Claude Code. Det er ikke bare Fabric (prompt-patterns) — det er infrastruktur for hvordan din AI opererer.

**Nøglearkitektur:**
- **TELOS** — 10 identitetsfiler (MISSION.md, GOALS.md, PROJECTS.md, BELIEFS.md, MODELS.md, STRATEGIES.md, NARRATIVES.md, LEARNED.md, CHALLENGES.md, IDEAS.md) der automatisk indlæses som kontekst
- **USER/SYSTEM separation** — brugertilpasning i USER/, systeminfrastruktur i SYSTEM/. Opgraderinger rører ikke personlige filer
- **6 lag customization:** Identity → Preferences → Workflows → Skills → Hooks → Memory
- **3-tier memory:** Hot (aktiv session) → Warm (nylig) → Cold (arkiv)
- **Hook system:** 8 lifecycle events (session start/end, tool use, task completion, context loading, security)
- **Skill hierarchy:** CODE → CLI tool → PROMPT → SKILL (prioriterer determinisme)

**Relevant for Ydrasil:** Vi har allerede CLAUDE.md + MEMORY.md + skills. PAI's TELOS-struktur er en formalisering af det vi gør uformelt. Vigtigste takeaway: **memory tiers** og **hooks der logger automatisk**.

### 1.2 GSD (Get Shit Done)

**Repo:** https://github.com/gsd-build/get-shit-done

Spec-drevet udviklingssystem for Claude Code. Løser "context rot" (kvalitet falder når context window fyldes).

**Nøglemønster:**
- **Spec-filer:** PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, PLAN.md, SUMMARY.md — hver med størrelsesbegrænsninger
- **Subagent orchestration:** Spawner friske Claude-instanser per opgave (rent 200k context window)
- **Wave-baseret parallelisering:** Uafhængige opgaver kører simultant, afhængige venter
- **Atomiske git commits:** Én commit per opgave, traceable messaging
- **XML task format:**
  ```xml
  <task type="auto">
    <name>Feature description</name>
    <files>target files</files>
    <action>Specific instructions</action>
    <verify>How to test</verify>
    <done>Success criteria</done>
  </task>
  ```

**Relevant for Ydrasil:** STATE.md-konceptet (cross-session memory af beslutninger og blockers) er præcis hvad vores NOW.md gør. Wave-parallelisering er overkill for os, men **friske subagenter** er interessant for tunge opgaver.

### 1.3 Claude Code Scheduler

**Repo:** https://github.com/jshchnz/claude-code-scheduler

Plugin der tilføjer scheduling direkte i Claude Code.

**Nøglefunktioner:**
- Natural language scheduling: "Run code review every weekday at 9am"
- Konverterer til platform-native cron (Linux: crontab)
- Autonomous mode: `--dangerously-skip-permissions`
- Git worktree isolation: Ændringer på separate branches
- Logs i `~/.claude/logs/<task-id>.log`

**Kommandoer:** `/scheduler:schedule-add`, `/scheduler:schedule-list`, `/scheduler:schedule-run <id>`

**Relevant for Ydrasil:** Vi har allerede vores egen cron-setup der er mere robust. Men worktree-isolation per opgave er en god idé.

### 1.4 Anthropic's Autonomous Coding Quickstart

**Repo:** https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding

Officiel reference-implementation.

**Two-agent pattern:**
1. **Initializer Agent** — læser spec, opretter feature_list.json med test cases, sætter projekt op
2. **Coding Agent** — picker næste feature, implementerer, markerer done, git commit, gentag

**Nøglemønstre:**
- Progress persisterer via `feature_list.json` + git commits
- Auto-continues mellem sessioner (3 sekunders delay)
- `Ctrl+C` pauser, samme kommando genoptager
- Defense-in-depth: OS sandbox + filesystem restrictions + command allowlist
- Hver iteration: 5-15 minutter

### 1.5 incident.io — Git Worktrees i Produktion

**Blog:** https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees

**Praktisk setup:**
- 4-5 Claude-agenter kører parallelt, hver i egen worktree
- Bash-funktion `w myproject new-feature claude` opretter branch + launcher Claude
- Plan Mode som sikkerhedsnet — lad Claude foreslå uden at udføre
- Voice dictation (SuperWhisper) → krav → Claude implementerer

### 1.6 Automated Claude Code Workers

**Blog:** https://www.blle.co/blog/automated-claude-code-workers

**Arkitektur:**
- Task Queue (MCP Server) → Cron Scheduler → Claude Worker Shell Script → Structured Prompts
- Cron hvert 10. minut: `*/10 * * * * /bin/zsh -l -c '/path/to/claude-worker.sh'`
- Login shell (`-l`) bevarer fuld udviklingsmiljø
- Prompt-filer i `/opt/claude-prompts/` der router per opgavetype

### 1.7 claude-flow (Multi-Agent Orchestration)

**Repo:** https://github.com/ruvnet/claude-flow

Tungt framework — 250.000+ linjer kode, 54+ specialiserede agenter. Overkill for os, men relevante koncepter:
- Background workers via WASM-backed retrieval
- Shared memory mellem agenter
- Offline-kapable med lokale modeller

**Verdict:** For komplekst til vores behov. Vores eksisterende cron + scripts setup er mere passende.

---

## 2. Claude Code Headless Mode — Det Praktiske

### 2.1 Basis-brug

```bash
# Simpel prompt, output til stdout
claude -p "Hvad gør auth-modulet?"

# Med tool-tilladelser
claude -p "Kør tests og fix fejl" --allowedTools "Bash,Read,Edit"

# Specifik tool-tilladelse (prefix matching med *)
claude -p "Lav commit" --allowedTools "Bash(git diff *),Bash(git commit *)"

# JSON output med session ID
claude -p "Opsummér projekt" --output-format json

# Fortsæt samtale
claude -p "Hvad med database queries?" --continue

# Genoptag specifik session
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')
claude -p "Fortsæt review" --resume "$session_id"

# Custom system prompt
claude -p "Review kode" --append-system-prompt "Du er sikkerhedsingeniør"

# Pipe input
cat data.csv | claude -p "Analysér denne data"
```

### 2.2 Vigtige Flags

| Flag | Funktion |
|------|----------|
| `-p` / `--print` | Headless mode (non-interactive) |
| `--allowedTools` | Auto-approve specifikke tools |
| `--output-format` | `text`, `json`, `stream-json` |
| `--continue` | Fortsæt seneste samtale |
| `--resume SESSION_ID` | Genoptag specifik session |
| `--append-system-prompt` | Tilføj system prompt |
| `--json-schema` | Struktureret output |
| `--dangerously-skip-permissions` | Skip alle tilladelser (autonomt) |

---

## 3. Hvad Vi Allerede Har (Ydrasil Status)

Vores eksisterende setup er faktisk ret avanceret sammenlignet med de fleste:

| Komponent | Status | Hvad andre kalder det |
|-----------|--------|----------------------|
| `trello_responder.sh` | Aktiv (hvert minut) | "Autonomous Claude Worker" |
| `trello_comment_watch.py` | Aktiv (hvert minut) | "Event Trigger / Inbox Pattern" |
| `voice_memo_pipeline.py` | Aktiv (hvert 2. min) | "File Watcher / Auto-process" |
| `morning_brief.py` | Aktiv (kl. 07:00) | "Scheduled Research" |
| `weekly_audit.py` | Aktiv (søndag 06:00) | "Scheduled Audit" |
| `auto_dagbog.py` | Aktiv (kl. 23:55) | "Daily Summary Agent" |
| `hotmail_autosort.py` | Aktiv (hver time :45) | "Email Automation" |
| `process_session_log.py` | Aktiv (hver 4. time) | "Session Memory / Embedding" |
| `sync_inbox.py` | Aktiv (kl. 07:05) | "Task Sync / Orchestration" |
| tmux pipe-pane logging | Aktiv (hver time) | "Persistent Session Logging" |
| CLAUDE.md + MEMORY.md | Aktiv | "Identity / Context Layer" |
| `.claude/skills/` | Aktiv | "Skill System" |
| NOW.md + checkpoints | Aktiv | "State Persistence" (GSD's STATE.md) |

**Konklusion:** Vi mangler ikke fundamentet. Vi mangler 3 ting:
1. **Claude-powered autonomi** (ikke bare Python-scripts, men Claude der tænker)
2. **Inbox-pattern for nye opgaver** (fil → auto-Claude)
3. **Worktree-isolation** for tunge opgaver

---

## 4. Konkret Implementeringsplan

### Fase 1: Claude Daemon (uge 1)

Opret en simpel daemon der tjekker for nye opgaver og kører Claude headless.

**Fil:** `scripts/claude_daemon.sh`

```bash
#!/bin/bash
# Claude Daemon — tjekker inbox og kører opgaver
# Cron: */5 * * * * /root/Ydrasil/scripts/claude_daemon.sh

export PATH="/root/.local/bin:$PATH"
cd /root/Ydrasil

INBOX="data/inbox"
LOCK="/tmp/claude_daemon.lock"
LOG="/var/log/ydrasil/claude_daemon.log"

# Lock-mekanisme (max 10 min)
if [ -f "$LOCK" ]; then
    lock_age=$(( $(date +%s) - $(stat -c %Y "$LOCK") ))
    if [ "$lock_age" -lt 600 ]; then
        exit 0
    fi
    rm -f "$LOCK"
fi

# Tjek for nye filer i inbox
shopt -s nullglob
files=("$INBOX"/*.md "$INBOX"/*.txt "$INBOX"/*.json)
shopt -u nullglob

if [ ${#files[@]} -eq 0 ]; then
    exit 0
fi

touch "$LOCK"

for file in "${files[@]}"; do
    filename=$(basename "$file")
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S')] Processing: $filename" >> "$LOG"

    # Kør Claude med filens indhold som opgave
    timeout 300 claude -p "$(cat "$file")

KONTEKST: Du er Kris' AI-assistent på VPS. Denne opgave kom via inbox.
REGLER:
1. Udfør opgaven. Gem resultater i data/ eller relevante mapper.
2. Rapportér kort hvad du har gjort.
3. Max 5 minutter per opgave." \
        --allowedTools "Bash,Read,Edit" \
        --output-format json 2>/dev/null | jq -r '.result' >> "$LOG"

    # Flyt til processed
    mkdir -p "$INBOX/processed"
    mv "$file" "$INBOX/processed/${filename}.$(date +%s)"

    echo "[$(date -u '+%Y-%m-%d %H:%M:%S')] Done: $filename" >> "$LOG"
done

rm -f "$LOCK"
```

**Cron:**
```
*/5 * * * * /root/Ydrasil/scripts/claude_daemon.sh 2>/dev/null
```

### Fase 2: Forbedret Trello-responder (uge 1-2)

Opgradér `trello_responder.sh` med:

1. **Session continuity** — Gem session_id, fortsæt samtaler
2. **Worktree for kodeændringer** — Når Kris beder om kode, kør i worktree
3. **Bedre tool-tilladelser** — Specifikke `--allowedTools` per opgavetype

```bash
# Forbedret responder med session continuity
SESSION_FILE="/tmp/trello_session_${card_id}"

if [ -f "$SESSION_FILE" ]; then
    session_id=$(cat "$SESSION_FILE")
    claude -p "$prompt" --resume "$session_id" --output-format json \
        --allowedTools "Bash,Read,Edit" | tee >(jq -r '.session_id' > "$SESSION_FILE")
else
    claude -p "$prompt" --output-format json \
        --allowedTools "Bash,Read,Edit" | tee >(jq -r '.session_id' > "$SESSION_FILE")
fi
```

### Fase 3: File Watcher med inotifywait (uge 2)

Mere responsiv end cron — reagerer øjeblikkeligt på nye filer.

**Fil:** `scripts/claude_watcher.sh` (kør som systemd service)

```bash
#!/bin/bash
# File watcher der trigger Claude på nye filer i inbox
export PATH="/root/.local/bin:$PATH"
cd /root/Ydrasil

INBOX="data/inbox"
mkdir -p "$INBOX" "$INBOX/processed"

inotifywait -m -e close_write -e moved_to "$INBOX" --format '%f' | while read filename; do
    # Skip ikke-tekstfiler
    case "$filename" in
        *.md|*.txt|*.json) ;;
        *) continue ;;
    esac

    file="$INBOX/$filename"
    [ -f "$file" ] || continue

    echo "[$(date)] New task: $filename" >> /var/log/ydrasil/watcher.log

    timeout 300 claude -p "$(cat "$file")

Du er Kris' AI-assistent. Opgave fra inbox. Udfør og rapportér." \
        --allowedTools "Bash,Read,Edit" >> /var/log/ydrasil/watcher.log 2>&1

    mv "$file" "$INBOX/processed/$filename.$(date +%s)"
done
```

**Systemd service:** `/etc/systemd/system/claude-watcher.service`
```ini
[Unit]
Description=Claude Code File Watcher
After=network.target

[Service]
Type=simple
ExecStart=/root/Ydrasil/scripts/claude_watcher.sh
Restart=always
RestartSec=10
User=root
WorkingDirectory=/root/Ydrasil

[Install]
WantedBy=multi-user.target
```

### Fase 4: Scheduled Research/Audit (uge 2-3)

Ugentlige autonome research-opgaver:

```bash
# Søndag kl 08:00 — ugentlig codebase-analyse
0 8 * * 0 claude -p "Analysér Ydrasil codebase:
1. Find dead code og ubrugte scripts
2. Tjek for sikkerhedsproblemer
3. Foreslå forenklinger
Skriv rapport til data/audits/audit_$(date +%Y-%m-%d).md" \
    --allowedTools "Bash,Read,Edit,Glob,Grep" \
    >> /var/log/ydrasil/auto_audit.log 2>&1

# Daglig kl 06:30 — kontekst-forberedelse inden morning brief
30 6 * * * claude -p "Forbered dagens kontekst:
1. Læs NOW.md for current state
2. Tjek Trello for deadlines og fokus
3. Opsummér i data/MORNING_BRIEF.md" \
    --allowedTools "Bash,Read,Edit" \
    >> /var/log/ydrasil/morning_prep.log 2>&1
```

### Fase 5: Worktree Pattern for Tunge Opgaver (uge 3)

Når Claude skal lave kodeændringer, brug worktree for isolation:

```bash
#!/bin/bash
# Kør Claude-opgave i isoleret worktree
TASK_NAME="${1:-auto-task}"
BRANCH="claude-task/${TASK_NAME}-$(date +%s)"
WORKTREE="/tmp/ydrasil-worktrees/$TASK_NAME"

cd /root/Ydrasil
git worktree add "$WORKTREE" -b "$BRANCH" HEAD

claude -p "$2" \
    --allowedTools "Bash,Read,Edit,Glob,Grep" \
    2>/dev/null

# Commit og cleanup
cd "$WORKTREE"
git add -A && git commit -m "Auto: $TASK_NAME" 2>/dev/null
cd /root/Ydrasil
git worktree remove "$WORKTREE" 2>/dev/null
echo "Branch: $BRANCH"
```

---

## 5. Prioriteret Anbefaling

**Start her (denne uge):**

1. **Claude Daemon inbox** — Enkleste win. Drop en .md fil i `data/inbox/`, Claude processor den. Kris kan sende opgaver fra telefonen via Telegram → fil → Claude.

2. **Opgradér trello_responder.sh** med `--continue`/`--resume` for samtale-continuity. Allerede 80% af vejen.

3. **Installér inotify-tools** (`apt install inotify-tools`) og sæt watcher op som systemd service. Mere responsivt end cron hvert minut.

**Uge 2-3:**

4. **Scheduled Claude audits** via cron. Simpelt — bare tilføj `claude -p` jobs til crontab.

5. **Git worktree wrapper** for kodeændringer. Vigtigst når Claude skal ændre webapp-filer der er live i produktion.

**Ikke nu:**

- claude-flow (for komplekst)
- GSD framework (overkill — vi har ikke et team)
- PAI installation (overlapper med vores eksisterende setup)
- claude-code-scheduler plugin (vi har bedre kontrol med egen crontab)

---

## 6. Sikkerhed og Guardrails

### Vigtige regler for autonom Claude:

1. **Altid timeout** — `timeout 300 claude -p ...` (5 min max). ALDRIG ubegrænset.
2. **Lock-filer** — Undgå overlappende kørsler. Check lock age, ryd stale locks.
3. **Begrænsede tools** — Brug `--allowedTools` specifikt. Aldrig `--dangerously-skip-permissions` i cron.
4. **Worktrees for kodeændringer** — Aldrig direkte ændringer til `/app/` fra autonom Claude.
5. **Logning** — Alt output til `/var/log/ydrasil/`. Roter logs ugentligt.
6. **Kris-godkendelse** — Autonom Claude foreslår, Kris godkender. Undtagen: Trello-svar, inbox-processing, audits.
7. **Omkostningskontrol** — Sæt dagligt API-budget. Tjek `data/cost_daily.json` inden kørsler.

---

## 7. Kris-specifik Anbefaling

Kris har ingen PC — kun Android + Termux. De vigtigste patterns:

- **Telegram → inbox/** — Send besked til bot → gemmes som .md i inbox → Claude processor
- **Trello-kommentar → Claude handler** — Allerede aktivt og virker
- **Voice memo → transcription → action** — Allerede aktivt (voice_memo_pipeline)
- **Google Tasks → sync** — Allerede aktivt (sync_inbox)

**Den manglende bro:** Kris kan ikke nemt give Claude *nye* typer opgaver uden at starte Claude Code interaktivt. Inbox-patternen løser dette: skriv opgaven som tekst, drop den i inbox, Claude udfører.

---

## Kilder

- [Daniel Miessler PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [GSD Framework](https://github.com/gsd-build/get-shit-done)
- [Claude Code Scheduler](https://github.com/jshchnz/claude-code-scheduler)
- [Anthropic Autonomous Coding Quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- [incident.io Git Worktrees Blog](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)
- [Automated Claude Code Workers](https://www.blle.co/blog/automated-claude-code-workers)
- [claude-flow](https://github.com/ruvnet/claude-flow)
- [Claude Code Headless Docs](https://code.claude.com/docs/en/headless)
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code Scheduler Feature Request #4785](https://github.com/anthropics/claude-code/issues/4785)
- [Running Claude Code 24/7](https://www.howdoiuseai.com/blog/2026-02-13-running-claude-code-24-7-gives-you-an-autonomous-c)
