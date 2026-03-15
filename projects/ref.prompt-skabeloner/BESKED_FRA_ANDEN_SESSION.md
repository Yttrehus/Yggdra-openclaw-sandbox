Denne besked er fra en anden Claude Code session (github-workflow). Læs og absorbér.

---

Jeg har forberedt en autonom VPS-kørsel for dit prompt-skabeloner projekt. Her er hvad jeg har gjort og hvad du skal vide:

## Hvad jeg har gjort

1. **Uploadet chatlog.md til VPS** — 21K linjer, ligger i `/root/Yggdra/yggdra-pc/chatlog.md`

2. **Skrevet prompt.md** — autonom mission i 6 iterationer (mine → kategorisér → byg skills → peer review). Ligger på VPS i `/root/Yggdra/yggdra-pc/prompt-skabeloner/prompt.md`. Inkluderer:
   - Dine kendte prompt-mønstre som udgangspunkt
   - Collector's Trap vakcinering (max 10 kandidater, max 5 skills)
   - Anti-patterns fra vps-sandbox-v2 (du skrev den)
   - Cross-session peer review absorberet som iteration 6
   - Output-struktur: `skills/` mappe med SKILL.md + references/

3. **Uploadet the-fool/SKILL.md som format-reference** — ligger i `prompt-skabeloner/reference-skill/`

4. **Oprettet STATE.md** på VPS — iteration 0, ikke startet

## Hvad jeg IKKE har gjort

- Ikke uploadet VPS chatlog (49K linjer) — overvej om det tilføjer værdi
- Ikke uploadet abstracts.json
- Ikke committet dit arbejde (CONTEXT.md, CLAUDE.md, brief-opdateringer) — det er dit ansvar
- Ikke startet VPS-sessionen — Yttre starter den fra telefon

## Vigtige detaljer

- **Ingen git på VPS.** `yggdra-pc/` er en undermappe i VPS'ens Ydrasil-repo (andet GitHub remote). Output er bare filer på disk. Yttre reviewer via SSH og flytter gode skills til PC repo bagefter.
- **Yttre slukker PC'en.** Han kører kun via SSH fra telefon. Alt skal være klart til én start-kommando.
- **Start-kommandoen:** `claude --dangerously-skip-permissions --print "Læs prompt-skabeloner/prompt.md og udfør missionen. Start med iteration 1."` fra `/root/Yggdra/yggdra-pc/`

## Hvad du bør gøre

1. **Læs prompt.md** — `ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/prompt-skabeloner/prompt.md"` — og vurdér om den matcher dit arbejde. Du har dybere kontekst om mønstrene end jeg har.
2. **Tilføj eller ret** hvad der mangler baseret på din sessions research (dialektisk analyse, explore-agent findings, planfil).
3. **Upload ændringer** hvis nødvendigt: `scp fil root@72.62.61.51:/root/Yggdra/yggdra-pc/prompt-skabeloner/`
4. **Commit dit eget arbejde** (CONTEXT.md, CLAUDE.md, denne fil, backlog-ændringer)
5. **Giv Yttre den endelige start-kommando**

## Fuld handoff-fil

Læs `projects/prompt-skabeloner/VPS_HANDOFF.md` for alle detaljer inkl. hvad der skete i min session (tags, branch workflow, PR #1, GitHub expertise research).
