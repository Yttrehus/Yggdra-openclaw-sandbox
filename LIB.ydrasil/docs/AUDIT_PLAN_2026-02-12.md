# Audit-plan — Februar 2026

**Dato:** 12. februar 2026
**Planlagt af:** Claude Opus 4.6
**Status:** PLAN v1 → Rød-hold → PLAN v2 → Rød-hold → Neutral → PLAN v3 (endelig)

---

## Proces (som Kris har defineret)

```
Plan v1 → Rødhold-kritik → Plan v2 → Rødhold-kritik → Neutral vurdering → Plan v3 (endelig)
```

Auditen gennemføres EFTER Kris har godkendt plan v3.

---

# PLAN v1

## Scope: 7 audit-domæner

### 1. Data-integritet: "Mister vi noget?"
**Fokus:** Alt der bør gemmes, bliver det reelt gemt?

- [ ] Test voice-filer: upload via webapp inbox, Telegram voice note, voice API — bliver de alle persisteret?
- [ ] Test transskriptioner: crasher sessionen, er transkriptionen gemt?
- [ ] Tjek Qdrant: er alle embeddings konsistente? Matcher antal punkter det forventede?
- [ ] Tjek backups: kl. 04:00 backup — virker den? Hvornår kørte den sidst? Hvad dækker den?
- [ ] Session-logs: er tmux pipe-pane aktiv? Timefiler roteret korrekt?

**Succeskriterium:** Nul data-tab. Upload en fil 5 steder, verificer den findes 5 steder.

### 2. Friktionsanalyse: "Hvor misforstår jeg Kris?"
**Fokus:** Analyse af alle tilgængelige sessioner for friction points.

- [ ] Gennemgå alle 62 JSONL-sessionsfiler kronologisk
- [ ] Identificer alle steder Kris var frustreret, uenig, eller ændrede retning
- [ ] Kategorisér friktionen: Misforståelse? Forkert prioritering? Discount-løsning? For langsom?
- [ ] Skriv kronologisk selvbiografi: "Hvordan jeg lærte Kris at kende"
- [ ] Opdatér KRIS_PROFILE.md med fund

**Succeskriterium:** Kris genkender sig selv i profilen og siger "ja, det er mig."

### 3. Forrige audits: "Hvad blev glemt?"
**Fokus:** Gennemgå alle 4 forrige audits og vurdér opfølgning.

| Audit | Fund | Status |
|-------|------|--------|
| 2026-02-01 | 41 items lukket, system-baseline | Implementeret |
| 2026-02-08 | Ukendt (tom/kort rapport) | Skal undersøges |
| 2026-02-10 | Tor eksponeret, API keys i git, forældet docs | Tor fixet, keys delvist fixet, docs delvist |
| 2026-02-11 | SSH-sikkerhed, n8n stadig aktiv | SSH fixet, n8n ukendt |

- [ ] For hver audit: hvad blev fundet, hvad blev fixet, hvad blev glemt?
- [ ] Nye issues fra i dag: lydfiler tabt, session crashes, agent timeouts
- [ ] Verificer: kører n8n stadig? (Den bør være stoppet)
- [ ] Verificer: er API keys gitignored korrekt?

**Succeskriterium:** Alle tidligere audit-fund har enten "fixet" eller "bevidst accepteret" status.

### 4. Hukommelses-audit: "Husker systemet det rigtige?"
**Fokus:** Test retrieval-kvalitet med kendte spørgsmål.

- [ ] Design 20 test-queries med kendte svar (10 rute-data, 5 advisor, 5 sessions)
- [ ] Kør `ctx` for hver query, bedøm relevans (1-5 skala)
- [ ] Gennemgå MEMORY.md, huskeliste.md, CLAUDE.md — er de opdaterede? Mangler noget?
- [ ] Tjek knowledge freshness: hvornår blev Nate/Miessler sidst opdateret?
- [ ] Sammenlign: hvad Kris har sagt vs. hvad systemet har husket

**Succeskriterium:** >80% af test-queries returnerer relevant kontekst i top-3 resultater.

### 5. Infrastruktur: "Er systemet sundt?"
**Fokus:** Sikkerhed, performance, pålidelighed.

- [ ] Port-scanning: hvad er eksponeret på internet?
- [ ] Docker: alle containers kører? Ingen unødvendige?
- [ ] Disk: plads, vækstrate, time-to-full
- [ ] Cron-jobs: hvilke kører, hvilke fejler, hvilke er deaktiverede?
- [ ] SSL/TLS: certifikat-status, HSTS, security headers
- [ ] API keys: korrekt opbevaret, roteret, gitignored?
- [ ] Voice API: uptime, error rate, responstider

**Succeskriterium:** Ingen kritiske sikkerhedsproblemer. Alle services kører.

### 6. Kilde-friskhed: "Er vores viden opdateret?"
**Fokus:** Hvornår blev videnskilderne sidst opdateret?

- [ ] Nate Jones: seneste transcript dato? Manglende videoer?
- [ ] Daniel Miessler: seneste blog post i systemet? Gap?
- [ ] Claude Code docs/best practices: outdated?
- [ ] youtube_monitor.py, source_discovery.py: status? (deaktiveret — bør genaktiveres?)

**Succeskriterium:** Klar plan for at holde kilder <7 dage bagud.

### 7. Automatiserings-muligheder: "Hvad kan automatiseres?"
**Fokus:** Alt der kører manuelt men kunne køre automatisk.

- [ ] Identificer gentagne manuelle opgaver
- [ ] Vurdér automatiseringspotentiale (simpel cron vs. LLM-in-loop)
- [ ] Estimér token-cost for automatisering
- [ ] Prioritér: høj-frekvens + lav-cost først
- [ ] Foreslå hierarkisk vidensindeks (sentinel agents) arkitektur

**Succeskriterium:** 3-5 konkrete automatiseringer klar til implementering.

---

## Metode

1. **Layer 1 research:** Bred scanning. Læs alle kilder. Noter alt der er off.
2. **Layer 2 deep-dive:** Gå dybt i hvert domæne. Kør tests. Verificer.
3. **Layer 3 syntese:** Saml fund. Prioritér. Skriv rapport.

**Mellem hvert layer:** Rapportér til Kris. Justér baseret på feedback.

---

## Estimeret tid

| Domæne | Estimat |
|--------|---------|
| 1. Data-integritet | 30 min |
| 2. Friktionsanalyse | 2-3 timer (62 sessioner) |
| 3. Forrige audits | 20 min |
| 4. Hukommelses-audit | 45 min |
| 5. Infrastruktur | 30 min |
| 6. Kilde-friskhed | 20 min |
| 7. Automatisering | 30 min |
| **Total** | **~5-6 timer** |

**Note:** Friktionsanalysen er den tungeste. Den kræver parsing af JSONL-filer som er i binært Claude Code format — skal undersøges om de kan læses.

---

# RØDHOLD-KRITIK v1

### Hvad er svagt i denne plan?

1. **Friktionsanalysen er for ambitiøs.** 62 JSONL-filer, mange i MB-størrelse, i proprietært format. Realistisk kan vi ikke parse dem alle. **Fix:** Start med de kilder vi *kan* læse: DAGBOG, Telegram-logs, voice diaries, og den nuværende sessions checkpoint. Det dækker ~60% af historikken.

2. **Ingen clear definition af "kritisk" vs "nice-to-have".** Planen lister 7 domæner uden at sige hvad der er vigtigst. **Fix:** Tier-0 (data-integritet, sikkerhed), Tier-1 (friktionsanalyse, hukommelse), Tier-2 (kilder, automatisering).

3. **"Succeskriterier" er vage.** ">80% af queries returnerer relevant kontekst" — hvad er "relevant"? Hvem bedømmer? **Fix:** Kris bedømmer. 20 queries med hans scoring.

4. **Mangler: Round Table.** Kris bad specifikt om multi-model consensus for vigtige beslutninger. Planen nævner det ikke. **Fix:** Tilføj Round Table som metode for audit-konklusioner.

5. **Mangler: Automatiserings-fokus.** Kris sagde audits skal så vidt muligt automatiseres. Planen er 100% manuel. **Fix:** For hvert fund, angiv om det kan automatisk monitoreres fremover.

6. **Tidsestimat er urealistisk.** 5-6 timer for en fuld audit er stramt. Friktionsanalysen alene kan tage en hel dag. **Fix:** Del auditen i 3 sessioner over 2-3 dage.

---

# PLAN v2 (efter rødhold)

## Ændringer fra v1

1. **Tiered prioritering:**
   - **Tier 0 (i dag):** Data-integritet + infrastruktur (30 min akut-scan)
   - **Tier 1 (næste session):** Friktionsanalyse + hukommelses-audit
   - **Tier 2 (session 3):** Kilder + automatisering + rapport

2. **Friktionsanalyse nedskaleret:** Brug DAGBOG + Telegram-logs + voice diaries + denne sessions kontekst. Ikke JSONL-parsing (endnu). Tilføj JSONL-parsing som separat research-opgave.

3. **Round Table tilføjet:** Audit-konklusioner sendes til 3 modeller (Claude, GPT-4o, Gemini) for uafhængig vurdering. Anonymiserede perspektiver.

4. **Automatiserings-flag:** Hvert fund markeres med:
   - `[A]` = kan automatiseres (foreslå script)
   - `[M]` = kræver manuel vurdering
   - `[AM]` = automatisk detection, manuel handling

5. **Sessionsplan:**
   - Session 1 (~1 time): Tier 0 akut-scan + rapportér til Kris
   - Session 2 (~2 timer): Friktionsanalyse + profil-iteration + hukommelses-test
   - Session 3 (~1.5 time): Kilder + automatisering + Round Table + endelig rapport

---

# RØDHOLD-KRITIK v2

### Hvad er stadig svagt?

1. **JSONL-parsing er udskudt, ikke løst.** De 62 sessioner indeholder den mest værdifulde data — Kris' faktiske ord og reaktioner. Uden dem er friktionsanalysen baseret på 2. hånds kilder (DAGBOG er mit perspektiv, ikke hans). **Modargument:** Det er bedre at starte med hvad vi har end at vente på en perfekt løsning. DAGBOG + voice diaries + denne session giver stadig 70% dækning. JSONL-parsing kan tilføjes som opfølgning.

2. **Round Table er overkill for en intern audit.** Multi-model consensus giver mening for strategiske beslutninger, ikke for "kører vores backup-cron?" **Modargument:** Enig — brug Round Table kun for de kvalitative konklusioner (friktionsanalyse, profil-vurdering), ikke for tekniske checks.

3. **3 sessioner over 2-3 dage er for spredt.** Kris mister kontekst mellem sessioner. **Modargument:** Hvad der er bedst for kvaliteten: frisk energi per session. Hvad Kris foretrækker: fokuseret burst. **Kompromis:** 2 sessioner — en i dag (Tier 0), en i morgen (resten).

4. **Planen nævner ikke hvem der ejer hvad.** Er det mig der gennemfører alt? Eller er der dele Kris skal gøre? **Fix:** Tilføj ejerskab per domæne.

---

# PLAN v3 (endelig, efter neutral vurdering)

## Neutral vurdering af v1 → v2 processen

Plan v1 var for bred og uden prioritering. Rødhold v1 fangede de vigtigste svagheder. Plan v2 tilføjede tiering, Round Table, og automatiserings-flag. Rødhold v2 nedskalerede Round Table og komprimerede tidsplanen. Den endelige plan er realistisk, fokuseret, og handler om det Kris faktisk har bedt om.

## Endelig audit-plan

### Session 1: Akut-scan (i dag, ~45 min)

**Ejer: Claude (autonom)**

| # | Check | Type | Succeskriterium |
|---|-------|------|-----------------|
| 1 | Voice-fil persistence | [A] | Upload fil via 3 kanaler, verificer alle gemt |
| 2 | Backup status | [A] | Backup kørte <24 timer siden, dækker /data/ + /app/ |
| 3 | Port-scanning | [A] | Ingen uventede porte eksponeret |
| 4 | Docker containers | [A] | Kun nødvendige kører, n8n stoppet |
| 5 | Disk + SSL | [A] | <80% disk, certifikat >30 dage |
| 6 | API keys | [M] | Ingen keys i git, .env korrekt |
| 7 | Cron-jobs status | [A] | Alle aktive jobs kører uden fejl |
| 8 | Voice API health | [A] | /health returnerer 200, <3s response |

**Output:** Akut-rapport med rød/gul/grøn status per check.

### Session 2: Dyb audit (næste session, ~2-3 timer)

**Ejer: Claude + Kris (iterativt)**

| # | Domæne | Type | Metode |
|---|--------|------|--------|
| 1 | Friktionsanalyse | [M] | Gennemgå DAGBOG, Telegram, voice diaries. Skriv selvbiografi. Præsentér profil for Kris' korrektion. |
| 2 | Hukommelses-audit | [AM] | 20 test-queries, Kris scorer relevans 1-5. Qdrant stats. |
| 3 | Forrige audits | [A] | Status-check på alle fund fra 4 audits. |
| 4 | Kilde-friskhed | [A] | Seneste dato per kilde. Gap-analyse. |
| 5 | Automatiserings-plan | [M] | Sentinel agent arkitektur. Hierarkisk indeks. Cost-estimat. |
| 6 | Round Table | [M] | Send friktions-konklusioner til 3 modeller. Konvergér. |

**Output:** Fuld audit-rapport + opdateret profil + automatiserings-roadmap.

### Automatisk overvågning (efter audit)

Implementér disse som permanente checks:

| Check | Frekvens | Script | Alert |
|-------|----------|--------|-------|
| Voice-fil persistence | Hver upload | Hook i upload-handler | Telegram-besked hvis fil mangler |
| Backup verification | Daglig kl. 04:30 | Cron | Telegram hvis backup fejler |
| Disk space | Daglig | weekly_audit.py | >85% = alert |
| Port exposure | Ugentlig | weekly_audit.py | Nye porte = alert |
| Qdrant health | Daglig | Cron | Collection counts + response time |
| Kilde-friskhed | Daglig | youtube_monitor.py | Gap >7 dage = flag |
| Token budget | Per run | cost_guardian.py | >80% budget = warning |

---

## Hvad auditen IKKE dækker (bevidst)

- **JSONL session-parsing:** Kræver separat research-opgave. JSONL-formatet er proprietært.
- **Google Drive integration:** Kris har nævnt det, men det kræver OAuth-setup som er et separat projekt.
- **Bogfører-robot:** Parkeret til efter voice + kontekst er på plads.
- **Hardware-anskaffelse:** Research, ikke audit.

---

*Klar til Kris' godkendelse. Skal session 1 (akut-scan) køres nu?*
