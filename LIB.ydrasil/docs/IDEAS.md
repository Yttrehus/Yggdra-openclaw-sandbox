# Master Ideas

Alle ideer, mål og planer samlet ét sted.

**Format:**
- Nyeste øverst
- Hver idé har: Titel, Dato, Beskrivelse, Status, Relaterede noter

---

## 2026-02-08: Dedikeret playbook for TransportIntra

**Type:** Dokumentation
**Status:** 🟡 I gang
**Beskrivelse:** Opret omfattende playbook-dokument der kortlægger hele TransportIntra projektet. Skal inkludere:
- Data-universet (API struktur, stop typer, status koder)
- Brugerscenarier (typisk arbejdsdag, problem-håndtering)
- Teknisk arkitektur (webapp stack, deployment)
- Features (route map, waypoints, GPS recording)

**Motivation:** Gøre det lettere for AI at forstå konteksten og hjælpe effektivt.

**Relateret:**
- `/root/transportintra-universe/brain/PLAYBOOK.md`
- Telegram bot diskussion 2026-02-08

---

## 2026-02-08: Auto-dagbog med idé-ekstraktion

**Type:** System forbedring
**Status:** 🟢 Implementeret
**Beskrivelse:** Udvid auto_dagbog.py til at:
1. Identificere ideer/mål/planer i dagens summaries
2. Tilføje dem til IDEAS.md med fuld forklaring
3. Reference dem kort i DAGBOG.md

**Motivation:** Centralisere alle ideer ét sted for bedre overblik.

**Implementering:**
- Haiku analyserer summaries for ideer
- Ekstraherer titel, beskrivelse, motivation
- Opdaterer både DAGBOG.md og IDEAS.md

---

*[Ældre ideer vil blive tilføjet automatisk fremover]*
