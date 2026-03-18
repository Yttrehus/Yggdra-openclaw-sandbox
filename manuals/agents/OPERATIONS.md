# Agent Operations Manual

Dette er manualen for autonome agenter, der opererer i Yggdra-systemet. Den indeholder standardprocedurer (SOPs), værktøjsoversigter og retningslinjer for kontinuitet.

## Hurtig oversigt over Agent-værktøjer

| Værktøj | Formål | Sti |
|---------|--------|-----|
| `checkpoint` | Skill til at gemme state og arkivere session | `.claude/skills/checkpoint.md` |
| `sitrep` | Skill til statusrapport over projektets sundhed | `.claude/skills/sitrep.md` |
| `session-resume` | Skill til hurtig genoptagelse af kontekst | `.claude/skills/session-resume.md` |
| `chatlog-engine` | Parser rå logs til læsbar `chatlog.md` | `projects/auto-chatlog/chatlog-engine.js` |
| `retrieval_poc` | Demonstration af Temporal Decay og Reranking | `scripts/retrieval_poc.py` |
| `fact_extraction` | Ekstraktion af fakta fra sessions (Gap 6) | `scripts/fact_extraction_poc.py` |

## Standardprocedurer (SOP)

### 1. Sessionsstart
1. Kør `/session-resume` for at indlæse de vigtigste state-filer.
2. Læs `DAGBOG.md` for de seneste personlige refleksioner.
3. Tjek `projects/0_backlog/TRIAGE.md` for prioriteringer.

### 2. Under sessionen
- Dokumentér alle væsentlige beslutninger i `DAGBOG.md` løbende.
- Vedligehold `CONTEXT.md` for det aktuelle overblik.
- Brug `scripts/pre_compact.sh` manuelt før compaction for at sikre chatlog-update.

### 3. Sessionsafslutning (Checkpoint)
- Kør altid `/checkpoint` som det sidste før sessionen lukkes.
- Sørg for at commit-beskeden er beskrivende for dagens fremdrift.

## Miljøspecifikke noter (Sandbox)
- Sessions-logs findes typisk i `/home/openclaw/.openclaw/agents/main/sessions/`.
- `chatlog-engine.js` er konfigureret til automatisk at detektere om den kører i OpenClaw sandbox eller lokalt.
