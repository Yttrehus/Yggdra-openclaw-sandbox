# VPS-PC Konvergensanalyse

**Dato:** 2026-03-14
**Status:** Anbefaling klar til beslutning

## 1. Fakta — hvad kører hvor

### VPS (Ydrasil) — drift og services
- **Docker:** 5 containers (traefik, nginx/webapp, qdrant, api-logger, tor-proxy)
- **Qdrant:** 7 collections, ~84K vektorer, hybrid search, temporal decay
- **Webapp:** TransportIntra LIVE produktion (volume-mounted, ændringer = deploy)
- **Cron:** ~18 aktive jobs: backup (04:00), dagbog (23:55), intelligence (06:30), YouTube monitor, source discovery, embedding, weekly audit, voice memo pipeline, hotmail autosort, daily sweep, cruft detector
- **Scripts:** 57 Python/bash scripts — embedding, research, telegram, voice, API logging
- **Hooks:** save_checkpoint.py (PreCompact/Stop) + load_checkpoint.sh (SessionStart) via Groq
- **Data:** credentials, route-data, episodes.jsonl (199+ episoder), intelligence briefings

### PC (Yggdra) — udvikling og kontekst
- **Hooks:** 4 registreret (pre_compact, post_session_check, session_start, session_end) — lokal episodisk log
- **Scripts:** 10 filer — hooks, Qdrant-søgning (via SSH tunnel), Notion API
- **Research:** 5 rapporter, INDEX.md med 5 atomiske noter, Zettelkasten-struktur
- **Projekter:** 3 aktive (context-engineering, research-architecture, mcp-skills-kompendium) + 15 backlog-briefs
- **Ingen Docker, ingen cron, ingen services**

### Overlap
- **Episodisk log:** Begge skriver episodes.jsonl, men uafhængigt (VPS via Groq, PC via git-diff)
- **Hook-system:** Begge har hooks, men forskelligt design og ingen synkronisering
- **CLAUDE.md:** Hver har sin egen — VPS fokuserer på drift, PC på udvikling
- **Research:** VPS har 60+ filer i research/, PC har 5 rapporter + arkiv af VPS-filer

### Unikke domæner
- **Kun VPS:** Webapp, Qdrant, Docker, cron jobs, Telegram, voice pipeline, embeddings, backup, API logging
- **Kun PC:** VS Code, lokal udvikling, Notion-integration, chatlog-engine, backlog-briefs

## 2. Tre mulige modeller

### Model A: PC overtager alt
PC bliver primær, VPS reduceres til hosting (webapp + Qdrant).
- **Fordel:** Ét sted for al udvikling og state
- **Ulempe:** Kræver migration af 57 scripts, 18 cron jobs, credentials. VPS skal stadig køre Docker. Kris har begrænset tid — migration er uger af arbejde med minimal ny værdi
- **Risiko:** Webapp er LIVE. Qdrant har 84K vektorer. Fejl under migration = nedetid

### Model B: Separate domæner (anbefalet)
VPS = drift og services. PC = udvikling og research. Ingen synkronisering af state.
- **VPS ejer:** Webapp, Qdrant, cron, embeddings, voice, telegram, backup, credentials
- **PC ejer:** Projekter, research, kontekst-engineering, hooks, lokal udvikling
- **Bro:** SSH (`ssh root@72.62.61.51 "command"`) + Qdrant tunnel for ctx-søgning
- **Fordel:** Intet at migrere. Begge kører som de er. Klarhed om hvad der hører hvor
- **Ulempe:** To episodiske logs, to CLAUDE.md'er — men det er allerede tilfældet og virker

### Model C: Synkroniseret
Git-baseret sync (rsync/pull) af udvalgte filer: episodes.jsonl, research/, NOW.md'er.
- **Fordel:** Begge instanser har fuld kontekst
- **Ulempe:** Merge-konflikter. Cron job til sync. State-divergens. Kompleksitet uden proportional værdi
- **Risiko:** Kris dropper ting med friktion (jf. Trello). Sync der fejler stille er værre end ingen sync

## 3. Anbefaling: Model B — Separate domæner

**Begrundelse:**
1. VPS er et modent driftsmiljø. Det virker. Der er ingen grund til at flytte det
2. PC er et udviklingsmiljø. Det bygger kontekst-engineering og research-praksis — ting der ikke kræver VPS-services
3. SSH-broen eksisterer allerede og bruges aktivt (ctx-søgning, remote commands)
4. Kris er solo-udvikler. Synkronisering er overhead der ikke giver proportional værdi
5. TRADEOFFS.md siger det selv: "Simplicitet > Features", "Ship iterativt"

**Grænsen er klar:** Hvis det kræver Docker, Qdrant, eller cron — det hører til VPS. Hvis det er research, projektstyring, eller lokal udvikling — det hører til PC.

## 4. Konkrete næste skridt

1. **Dokumentér domæneopdeling i begge CLAUDE.md'er** — tilføj 3 linjer der siger "VPS ejer drift, PC ejer udvikling, SSH er broen". Gør det eksplicit så fremtidige sessioner ikke genopfinder spørgsmålet
2. **PC session_start.sh: hent VPS-episoder via SSH** — scriptet har allerede SSH-kald som kommentar. Uncomment det. Det giver PC kontekst fra VPS-sessioner uden sync
3. **Consolidér research/** — VPS har 60+ filer, PC har 5 + arkiv. Beslut: er VPS-research "done" (frosset arkiv) eller aktivt? Anbefaling: frys VPS-research, al ny research sker på PC
4. **Ryd Trello-cruft på VPS** — 5+ cron jobs poller Trello som er droppet. Fjern dem. Nul risiko, sparer CPU
5. **Tilføj `vps` alias til PC** — `alias vps="ssh root@72.62.61.51"` i .bashrc/.zshrc. Reducerer friktion for den daglige bro
