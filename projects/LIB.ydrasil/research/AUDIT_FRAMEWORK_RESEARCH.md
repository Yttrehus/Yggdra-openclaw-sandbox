# Research: Audit af audit-processen — Bedste praksis for solo-udviklere

## Sammenfatning

Vores eksisterende audit (2026-02-01) er grundig og handlingsorienteret. Den dækker infrastruktur, scripts, dokumentation, filstruktur og hooks. Men der er dimensioner den mangler, og strukturelle forbedringer der kan gøre fremtidige audits mere systematiske.

---

## 1. Hvad den nuværende audit gør godt

- **Konkret og handlingsbar**: Prioriteret handlingsplan med "NU / snart / kan vente"
- **Tabel-drevet**: Let at skimme, klar status per komponent
- **Root cause-analyse**: Identificerer dokumentations-drift som hovedproblem
- **Operationelt fokus**: Tjekker reelle services, porte, cron, disk

---

## 2. Dimensioner der mangler

### A. Sikkerhed (delvist dækket, men overfladisk)
- **Exposed endpoints**: Hvad kan nås udefra?
- **Secrets management**: Hardcoded credentials i scripts?
- **SSL/TLS status**: Udløb, konfiguration
- **Qdrant access control**: Er port 6333 kun tilgængelig lokalt?

### B. Operational Resilience / Recovery
- **Backup verification**: Kører backup — men virker restore? Test det.
- **Mean Time to Recovery (MTTR)**: Hvis VPS'en dør, hvor lang tid tager det at genskabe alt?
- **Failure modes**: Hvad sker der hvis Qdrant crasher? Hvis disk fyldes?
- **Monitoring/alerting**: Hvem får besked når noget fejler?

### C. Cost Tracking & Drift
- Trend over tid (stiger/falder?)
- Cost per komponent (OpenAI, Hostinger, domæne)
- Budget/threshold alerts

### D. Documentation Drift (målt, ikke kun observeret)
Inspiration fra evolutionary architecture fitness functions:
- **Fitness function**: "Antal referencer til afviklede systemer (n8n) i docs = 0"
- **Fitness function**: "Alle kørende services er dokumenteret i infrastructure skill"
- Disse kan automatiseres som et script der kører ved audit.

### E. Systemets "Purpose Alignment"
Nate B. Jones' Second Brain framework fokuserer på: Løser systemet faktisk det problem det skal?
- Bruger Kris faktisk webapp'en dagligt?
- Hvilke features bruges, hvilke er ubrugte?
- Sparer det tid på ruten?

---

## 3. Anbefalet audit-framework: 7 dimensioner

Baseret på DORA metrics, fitness functions og Miessler's PAI-tilgang:

| # | Dimension | Vægt | Målbar? | Nuværende audit |
|---|-----------|------|---------|-----------------|
| 1 | **Operational Health** (services kører, disk OK, cron OK) | Høj | Ja — automatiseret | Godt dækket |
| 2 | **Documentation Accuracy** (docs matcher virkelighed) | Høj | Ja — kan scriptes | Dækket, men manuelt |
| 3 | **Security Posture** (auth, secrets, exposure) | Høj | Delvist | Overfladisk |
| 4 | **Recovery Readiness** (backup virker, MTTR kendt) | Høj | Ja — test restore | Mangler |
| 5 | **Code Hygiene** (dead code, duplikater, fejlhåndtering) | Medium | Ja | Godt dækket |
| 6 | **Cost Efficiency** (trend, budget, alerts) | Medium | Ja — CostGuardian data | Minimal |
| 7 | **Purpose Alignment** (bruges det? virker det?) | Medium | Delvist — usage logs | Mangler |

### DORA metrics tilpasset solo-udvikler

| DORA metric | Solo-tilpasning | Relevant? |
|-------------|-----------------|-----------|
| Deployment Frequency | Antal commits/deploys per uge | Ja — volume mount = deploy |
| Lead Time for Changes | Tid fra idé til produktion | Mindre relevant |
| Change Failure Rate | Hvor ofte ødelægger en ændring noget? | Ja — kræver logging |
| Time to Restore (MTTR) | Tid til at fikse når noget går ned | Kritisk |

---

## 4. Fitness Functions (konkrete forslag)

```python
# Eksempler på fitness functions der kan køre som del af /audit

# 1. Doc drift: Ingen n8n-referencer i aktive docs
assert grep_count("n8n", "CLAUDE.md") == 0
assert grep_count("n8n", ".claude/skills/") == 0

# 2. Alle systemd services er dokumenteret
running_services = get_systemd_services()
documented_services = parse_infrastructure_skill()
assert running_services.issubset(documented_services)

# 3. Ingen hardcoded secrets
assert grep_count("OPENAI_API_KEY.*=.*sk-", "scripts/") == 0

# 4. Backup freshness
assert backup_age_hours() < 28  # Max 28 timer gammel

# 5. Qdrant health
for collection in ["routes", "conversations", "sessions"]:
    assert qdrant_status(collection) == "green"

# 6. Cost trend
assert monthly_cost_trend() < 1.2  # Max 20% stigning
```

---

## 5. Praktiske anbefalinger

### Gør /audit smartere
Udvid det nuværende `/audit` command med:
1. Documentation drift detection (grep for kendte forældede termer)
2. Security quick-scan (exposed ports, CORS config)
3. Backup freshness check
4. Cost trend fra `cost_daily.json`

### Meta-kriterier: Audit af auditen
1. **Komplethed**: Dækker den alle 7 dimensioner?
2. **Målbarhed**: Kan resultaterne sammenlignes med forrige audit?
3. **Automatisering**: Hvor meget kører automatisk vs. manuelt?
4. **Handlingsbarhed**: Har hvert fund en prioritet og en "fix"?
5. **Feedback loop**: Blev sidste audits findings faktisk fikset?

### Frekvens
- **Daglig**: Operational health (allerede automatiseret via cron)
- **Ugentlig**: Fuld 7-dimensions audit (udvid `/audit`)
- **Månedlig**: Purpose alignment review (bruger Kris det?)

---

## 6. Miessler's "LLM-as-Judge" tilgang

Lad Claude læse forrige audit + nuværende systemtilstand og vurdere:
- Hvilke findings fra sidst er fikset?
- Hvilke er nye?
- Hvad er regression?

Dette giver automatisk en **delta-audit** fremfor at starte fra scratch.

---

## Kilder

- [Imaginovation — Software Audit Guide](https://imaginovation.net/blog/software-audit-guide/)
- [KOMODO — 10-Point Software Audit Checklist](https://www.komododigital.co.uk/resources/comprehensive-10-point-software-audit-checklist)
- [Daniel Miessler — Personal AI Infrastructure](https://danielmiessler.com/blog/personal-ai-infrastructure)
- [Daniel Miessler — LLM-as-Judge Evals](https://danielmiessler.com/blog/using-the-smartest-ai-to-rate-other-ai)
- [Nate B. Jones — Second Brain Guide](https://www.natebjones.com/prompts-and-guides/products/second-brain)
- [DORA — Software Delivery Performance Metrics](https://dora.dev/guides/dora-metrics-four-keys/)
- [InfoQ — Fitness Functions for Architecture](https://www.infoq.com/articles/fitness-functions-architecture/)
- [Tim Sommer — Using Fitness Functions](https://www.timsommer.be/using-fitness-functions-to-create-evolving-architectures/)
- [Redwerk — SDLC Audit Checklist](https://redwerk.com/blog/sdlc-audit-checklist-auditing-the-software-development-process/)
