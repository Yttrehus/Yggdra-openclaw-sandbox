# VPS Handoff — Prompt-skabeloner

Skrevet af session (github-workflow, 2026-03-14).

---

## Kontekst fra denne session

### Hvad vi lavede
1. **GitHub expertise:** Yttre ville vide hvordan professionelle bruger GitHub med Claude Code. Gennemgik git worktrees, branch workflow, PR-based review, parallel agents.
2. **Tags implementeret:** `session-13..18` tagget og pushet til GitHub. Fremover: `git tag session-XX` ved session-slut.
3. **Branch workflow demonstreret:** Første PR (#1) — README opdateret. Branch → PR → merge → cleanup. Yttre har set hele flowet.
4. **Cross-session peer review absorberet:** `brief.cross-session-peer-review.md` er absorberet i prompt-skabeloner. Bagt ind som iteration 6 i VPS prompt.md.
5. **VPS-pakke uploadet:** chatlog + prompt.md + reference-skill allerede på VPS.

### Beslutninger
- Branch workflow fra nu af på PC-repo (main = rent, feature branches for arbejde)
- VPS kører autonomt, filer på disk, IKKE git/repo — bare output i mappen
- Yttre starter fra telefon via SSH efter PC slukkes

---

## Hvad er på VPS (`/root/Yggdra/yggdra-pc/`)

```
chatlog.md                              ← 21K linjer PC chatlog
prompt-skabeloner/
├── prompt.md                           ← autonom mission (6 iterationer)
├── STATE.md                            ← progress tracker (iteration 0)
└── reference-skill/
    └── SKILL.md                        ← the-fool som format-reference
```

### prompt.md opsummering
- **Iteration 1:** Mine chatlog for gentagne Yttre-mønstre (>100 ord beskeder)
- **Iteration 2:** Kategorisér: kompleks (skill) vs. simpel (one-liner)
- **Iteration 3-5:** Byg ét skill per iteration (SKILL.md + references/)
- **Iteration 6:** Peer review + collector's trap check
- **Output:** `skills/` mappe med færdige skills, `MINING_RESULTS.md`, `EVALUATION.md`
- **Anti-patterns bagt ind:** fra v1 sandbox learnings

---

## Hvad DU (denne session) skal gøre

### 1. Review prompt.md
```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/prompt-skabeloner/prompt.md"
```
Har du kontekst fra din session der bør ind? Specifikke mønstre du fandt? Opdatér og upload:
```bash
scp fil root@72.62.61.51:/root/Yggdra/yggdra-pc/prompt-skabeloner/prompt.md
```

### 2. Upload ekstra filer hvis nødvendigt
VPS'en har chatlog.md + the-fool reference. Den mangler:
- Evt. VPS chatlog (`projects/ydrasil/vps-chatlog.md`) — 49K linjer ekstra data
- Evt. abstracts.json — hurtig session-scanning

Overvej om det tilføjer værdi eller bare er noise.

### 3. Commit dit eget arbejde
Du har ucommittede filer:
- `projects/prompt-skabeloner/CLAUDE.md`
- `projects/prompt-skabeloner/CONTEXT.md`
- `projects/prompt-skabeloner/VPS_HANDOFF.md`
- `projects/0_backlog/brief.research-architecture.md` (ændret)
- `projects/0_backlog/vps-sandbox-v2.md` (nyt)

### 4. Giv Yttre start-kommandoen
Yttre starter fra telefon:
```bash
ssh root@72.62.61.51
cd /root/Yggdra/yggdra-pc
claude --dangerously-skip-permissions --print "Læs prompt-skabeloner/prompt.md og udfør missionen. Start med iteration 1."
```

### 5. Opdatér CONTEXT.md
Notér at VPS-session er klar. Yttre starter den manuelt.

---

## Når VPS er færdig

Yttre reviewer via SSH:
```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/prompt-skabeloner/STATE.md"
ssh root@72.62.61.51 "ls /root/Yggdra/yggdra-pc/prompt-skabeloner/skills/"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/prompt-skabeloner/EVALUATION.md"
```

Gode skills flyttes til PC repo: `.claude/skills/` via SCP.
