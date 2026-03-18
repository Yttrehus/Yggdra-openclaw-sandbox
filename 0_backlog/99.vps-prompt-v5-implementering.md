# VPS Ralph Loop — V5 Implementering

Deploy til `/root/Yggdra/yggdra-pc/v5-implementering/`.
5 iterationer. BUILD — dette er kode, ikke research.

---

## CLAUDE.md

```markdown
# V5 Implementering — Sandbox

Du kører autonomt i en Ralph loop. Yttre er ikke tilgængelig.
Hver iteration er et `claude --print` kald.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten
2. Læs LOOP_STATE.md — check ## Blokkere
3. Læs den relevante iteration i LOOP_PLAN.md
4. VALIDÉR INPUT: Check at filer fra forrige iteration eksisterer
5. Udfør opgaven. Skriv/ændr kode
6. TEST med kommandoer (python3 -c "...", crontab -l, curl, grep)
7. Opdatér LOOP_STATE.md
8. Stop

## LOOP_STATE format

```
# Loop State
## Blokkere
(ingen / liste)

## Filregister
(kumulativ liste af ændrede filer)

## Iteration [N-1] (seneste)
Opgave: ...
Output: ...
Done: ... → PASS/FAIL

## Iteration [N-2]
(slet ældre end N-2)

## Næste: Iteration N
```

## Projekt

Implementér 5 konkrete forbedringer i eksisterende VPS-scripts. Alt er baseret på V4 research (PIPELINE_DESIGN.md, GAPS.md, WHAT_IF.md). Koden eksisterer allerede — du udvider den.

## Regler

### Token-bevidsthed
- Læs ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Build > Research
- Hver iteration SKAL ændre kode eller config på disk
- Ingen rapporter — kun kode, config, og test-resultater

### Done = Verified
- Test ALTID med `python3 -c "..."` eller direkte kørsel
- Verificér at ændringer ikke bryder eksisterende funktionalitet
- Kør eksisterende script med --test eller --dry-run hvis muligt

### Miljø
- Du er PÅ VPS'en. ALDRIG ssh til dig selv
- SØG IKKE på nettet
- Python venv: /root/Yggdra/scripts/venv/bin/python3
- Scripts: /root/Yggdra/scripts/
- Config: /root/Yggdra/data/intelligence_sources.json
- Crontab: `crontab -l` og `crontab -e` (brug `(crontab -l; echo "...") | crontab -`)
- Qdrant: curl localhost:6333/collections

### Anti-patterns
- OMSKRIV IKKE hele scripts — tilføj/ændr funktioner
- TEST før du ændrer crontab
- Tag BACKUP af filer du ændrer (`cp file file.bak`)
- Brug IKKE pip install uden at teste først
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — V5 Implementering (5 iterationer)

## Iteration 1 — Genaktivér heartbeat + morning_brief
**Opgave:** Uncomment heartbeat.py og morning_brief.py i crontab. Test begge.
**Metode:**
1. `cp /var/spool/cron/crontabs/root /tmp/crontab.bak` (backup)
2. Læs `head -30 /root/Yggdra/scripts/heartbeat.py` — forstå hvad den gør
3. Læs `head -30 /root/Yggdra/scripts/morning_brief.py` — forstå hvad den gør
4. Test heartbeat: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/heartbeat.py` (observer output)
5. Test morning_brief: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/morning_brief.py` (observer output)
6. Hvis begge kører uden crash: uncomment i crontab
7. Verificér: `crontab -l | grep -v '^#' | grep -c 'heartbeat\|morning_brief'` → 2
**Done:** Begge uncommented i crontab, begge testet uden crash

## Iteration 2 — Temporal decay i get_context.py
**Opgave:** Tilføj recency-weighting til Qdrant retrieval i get_context.py
**Metode:**
1. `cp /root/Yggdra/scripts/get_context.py /root/Yggdra/scripts/get_context.py.bak`
2. `grep -n 'def.*search\|def.*query\|score\|payload' /root/Yggdra/scripts/get_context.py` — find retrieval-logik
3. Find hvor scores returneres fra Qdrant
4. Tilføj decay: `score *= math.exp(-age_days / 30)` hvor age_days beregnes fra payload timestamp
5. Håndtér manglende timestamps gracefully (default: ingen decay)
6. Test: `python3 -c "from get_context import ...; ..."` eller `ctx "test query"` og verificér at nyere resultater scorer højere
**Output:** Opdateret get_context.py med temporal decay
**Done:** get_context.py ændret, test viser at nyere resultater prioriteres, eksisterende queries stadig virker

## Iteration 3 — Pipeline health check i daily_sweep.py
**Opgave:** Tilføj check i daily_sweep.py der alerter hvis pipelines ikke har produceret output
**Metode:**
1. `cp /root/Yggdra/scripts/daily_sweep.py /root/Yggdra/scripts/daily_sweep.py.bak`
2. `head -60 /root/Yggdra/scripts/daily_sweep.py` — forstå strukturen
3. Tilføj funktion `check_pipeline_health()`:
   - Check at `data/intelligence/daily_YYYY-MM-DD.md` eksisterer (ai_intelligence output)
   - Check at `data/intelligence/youtube_YYYY-MM-DD.md` eksisterer (youtube_monitor output)
   - Hvis BEGGE mangler for i dag OG i går: log WARNING
   - Check /var/log/ydrasil/intelligence.log for errors i seneste 48 timer
4. Tilføj kaldet i main-flow
5. Test: `python3 daily_sweep.py --test` eller direkte kørsel
**Output:** Opdateret daily_sweep.py
**Done:** Health check kører, rapporterer status korrekt

## Iteration 4 — Blog RSS feeds
**Opgave:** Tilføj 4 blog RSS feeds til sources.json og verificér at fetch_rss() henter dem
**Metode:**
1. `cp /root/Yggdra/data/intelligence_sources.json /root/Yggdra/data/intelligence_sources.json.bak`
2. Tilføj til rss_feeds-sektionen i sources.json:
   - Anthropic Research: https://www.anthropic.com/research/rss (priority: high)
   - OpenAI Blog: https://openai.com/blog/rss/ (priority: high)
   - Google DeepMind: https://deepmind.google/blog/rss.xml (priority: medium)
   - Hugging Face Blog: https://huggingface.co/blog/feed.xml (priority: medium)
3. Test hver feed: `python3 -c "import feedparser; f=feedparser.parse('URL'); print(len(f.entries), f.entries[0].title if f.entries else 'EMPTY')"`
4. Kør fetch_rss isoleret: `python3 -c "import sys; sys.path.insert(0,'/root/Yggdra/scripts'); from ai_intelligence import fetch_rss; items=fetch_rss(); print(len(items), 'items')"`
5. Verificér: `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d.get('rss_feeds',[])), 'feeds')"` → mindst 6
**Output:** Opdateret sources.json + test-resultater
**Done:** 4 nye feeds tilføjet, alle returnerer data, fetch_rss() henter dem

## Iteration 5 — Discovered sources cleanup + review
**Opgave:** Rens discovered_sources i sources.json. Review alle ændringer.
**Metode:**
1. `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d.get('discovered_sources',[])), 'discovered')"`
2. Fjern entries med noise-navne ("prize", "Tools/Platforms", "Ukendt kanal", "ikke specificeret")
3. Behold kun entries med reelle navne og URLs
4. Review alle ændringer fra iteration 1-4:
   - `crontab -l | grep -v '^#'` — verificér heartbeat + morning_brief aktive
   - `diff /root/Yggdra/scripts/get_context.py.bak /root/Yggdra/scripts/get_context.py` — review decay-ændring
   - `diff /root/Yggdra/scripts/daily_sweep.py.bak /root/Yggdra/scripts/daily_sweep.py` — review health check
   - `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d.get('rss_feeds',[])), 'feeds,', len(d.get('discovered_sources',[])), 'discovered')"` — tæl feeds og sources
5. Skriv REVIEW.md med samlet status
**Output:** Renset sources.json + REVIEW.md
**Done:** discovered_sources renset, alle 4 iterationers ændringer verificeret, REVIEW.md skrevet
```

---

## LOOP_STATE.md (initial)

```markdown
# Loop State

## Blokkere
(ingen)

## Filregister
(tomt)

## Næste: Iteration 1
Genaktivér heartbeat + morning_brief
```

---

## Start-kommando

```bash
mkdir -p /root/Yggdra/yggdra-pc/v5-implementering
cd /root/Yggdra/yggdra-pc/v5-implementering

# Deploy CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md først

for i in $(seq 1 5); do
  echo "=== Iteration $i === $(date)"
  if grep -q "BLOCKED\|FAILED" LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED ==="
    cat LOOP_STATE.md | head -10
    break
  fi
  timeout 600 /root/.local/bin/claude --print \
    "Du er iteration $i af 5. Følg CLAUDE.md boot-sekvens."
  if ! grep -q "Iteration $i" LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi
  echo "=== Iteration $i done === $(date)"
  sleep 10
done
```

---

## Review fra telefon

```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/v5-implementering/LOOP_STATE.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/v5-implementering/REVIEW.md"
ssh root@72.62.61.51 "crontab -l | grep -v '^#' | wc -l"
ssh root@72.62.61.51 "diff /root/Yggdra/scripts/get_context.py.bak /root/Yggdra/scripts/get_context.py | head -30"
```
