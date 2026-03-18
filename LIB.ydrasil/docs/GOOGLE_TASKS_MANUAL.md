# Google Tasks — Manual for Kris & Claude

**Oprettet:** 21. februar 2026
**Status:** Aktiv — erstatter Trello som primær task-manager

---

## Hvorfor Tasks i stedet for Trello?

| | Trello | Google Tasks |
|---|---|---|
| **Adgang** | Web + app | Indbygget i Gmail, Calendar, mobil-widget |
| **Hastighed** | Tungt UI, mange klik | Lynhurtig, minimal UI |
| **Kalender-integration** | Tredjepart (Power-Up) | Native — tasks med frist vises direkte i Google Calendar |
| **CLI-adgang (Claude)** | API med board/list/card-hierarki | Simpelt REST API, ét script |
| **Offline** | Nej | Ja (Android app) |
| **Pris** | Gratis (begrænset) | Gratis, ubegrænset |
| **Subtasks** | Checklists (begrænset) | Ægte subtasks med hierarki |
| **Kompleksitet** | Boards → Lists → Cards → Labels → Members | Lister → Tasks → Subtasks. Færdig. |

**Bundlinje:** Trello er godt til team-boards med mange kolonner. Til personlig task-management er Google Tasks hurtigere, enklere, og bedre integreret.

---

## Hvor finder du Google Tasks?

### På telefon
1. **Google Tasks app** — dedikeret app (installer fra Play Store)
2. **Gmail app** — tryk på Tasks-ikonet i bunden
3. **Google Calendar app** — tasks med frist vises som events
4. **Widget** — tilføj Google Tasks widget på homescreen for hurtig adgang

### I browser
1. **Gmail** → højre sidebar → Tasks-ikon (afkrydsningsfelt)
2. **Google Calendar** → tasks vises på datoen
3. **tasks.google.com** — standalone web-app

### Fra Claude (CLI)
```bash
python3 scripts/integrations/google_tasks.py show          # Vis alle
python3 scripts/integrations/google_tasks.py add "Titel"   # Tilføj
python3 scripts/integrations/google_tasks.py done TASK_ID   # Færdig
```

---

## Grundlæggende brug

### Opret task
- **Telefon:** Åbn Tasks → tryk + → skriv titel → gem
- **Gmail:** Sidebar → Tasks → tryk + → skriv titel
- **Claude:** `python3 google_tasks.py add "Titel" --notes "Detaljer" --due 2026-02-25`

### Tilføj detaljer
Hver task har:
- **Titel** — kort, handlingsorienteret ("Ring til forsikring")
- **Beskrivelse** — detaljer, links, kontekst
- **Frist (dato)** — vises i Calendar
- **Subtasks** — del store tasks op i trin

### Markér færdig
- **Telefon:** Tryk på cirklen til venstre for tasken
- **Claude:** `python3 google_tasks.py done TASK_ID`
- Færdige tasks forsvinder fra listen (kan gendannes)

### Gentag / genåbn
- **Telefon:** Gå til "Fuldførte" → tryk på task → "Markér som ikke fuldført"
- **Claude:** `python3 google_tasks.py undone TASK_ID`

---

## Tips & Tricks

### 1. Brug frister strategisk
Tasks med frist vises i Google Calendar. Det giver overblik over hvad der skal ske hvornår — uden at du skal åbne Tasks-appen.

**Pro tip:** Sæt fristen til den dag du vil *gøre* opgaven, ikke den dag den skal være færdig. Så bliver Calendar din daglige to-do.

### 2. Subtasks til store projekter
Eksempel:
```
[ ] Feedback-app til personalmøde (frist: 27/2)
    [ ] Design simpelt login-flow
    [ ] Byg voice-memo upload
    [ ] Test transkription
    [ ] Lav præsentation
```

Subtasks nedarver IKKE frist fra parent — sæt frister individuelt.

### 3. Flere lister til forskellige kontekster
Forslag:
- **Arbejde** — TransportIntra, ruter, firma-ting
- **Projekter** — Feedback-app, kompendium, rejsebureau
- **Personligt** — privat, hjem, aftaler

Opret nye lister: Tasks-app → hamburger-menu → "Opret ny liste"

### 4. Widget på homescreen
Den allervigtigste funktion. Sæt Google Tasks widget på din Android-homescreen:
1. Long-press på homescreen → Widgets
2. Find "Tasks" → træk den på plads
3. Vælg hvilken liste der vises

Nu ser du dine tasks HVER gang du åbner telefonen.

### 5. Drag-and-drop sortering
I Tasks-appen kan du trække tasks op/ned for at ændre prioritet. Den øverste task er den vigtigste.

### 6. "Markér som e-mail" i Gmail
I Gmail kan du markere en email som task: Åbn email → tre-prik-menu → "Tilføj til Tasks". Emailen linkes direkte i tasken.

### 7. Hurtig tilføjelse via Calendar
I Google Calendar: klik/tryk på en dato → vælg "Task" i stedet for "Event" → skriv titel. Done.

---

## Vores setup (Kris + Claude)

### Lister
| Liste | Formål |
|-------|--------|
| tasks for yttre | Standard/generel liste |

*(Vi opretter flere lister efter behov)*

### Workflow
1. **Kris** tilføjer tasks fra telefon (Tasks-app, widget, eller voice memo → Claude konverterer)
2. **Claude** tilføjer tasks via CLI-script baseret på samtaler og voice memos
3. **Frister** synkroniseres automatisk til Google Calendar
4. **Daglig review:** Claude kan vise status ved session-start

### Claude CLI-reference

```bash
# Vis tasks
python3 scripts/integrations/google_tasks.py show
python3 scripts/integrations/google_tasks.py show --all    # inkl. afsluttede

# Tilføj
python3 scripts/integrations/google_tasks.py add "Titel"
python3 scripts/integrations/google_tasks.py add "Titel" --notes "Detaljer" --due 2026-02-25
python3 scripts/integrations/google_tasks.py add "Subtask" --parent PARENT_TASK_ID

# Opdater
python3 scripts/integrations/google_tasks.py update TASK_ID --title "Ny titel"
python3 scripts/integrations/google_tasks.py update TASK_ID --notes "Nye noter"
python3 scripts/integrations/google_tasks.py update TASK_ID --due 2026-03-01

# Status
python3 scripts/integrations/google_tasks.py done TASK_ID
python3 scripts/integrations/google_tasks.py undone TASK_ID

# Slet
python3 scripts/integrations/google_tasks.py delete TASK_ID

# Lister
python3 scripts/integrations/google_tasks.py lists
python3 scripts/integrations/google_tasks.py newlist "Projekter"

# Flyt task til anden liste
python3 scripts/integrations/google_tasks.py move TASK_ID --to LIST_ID

# Ryd afsluttede
python3 scripts/integrations/google_tasks.py clear
```

---

## Begrænsninger (vs. Trello)

- **Ingen labels/tags** — Tasks har ikke farve-labels. Brug lister i stedet.
- **Ingen kommentarer** — kun én notes-felt per task. Brug notes til løbende opdateringer.
- **Ingen tildelinger** — Tasks er personlige. Ingen "assign to person". (Det er fint — det er din personlige liste.)
- **Ingen boards/kolonner** — ingen kanban-visning. Tasks er en lineær liste. Brug "Fuldført" som din "Done"-kolonne.
- **Ingen gentagelse via API** — gentagne tasks kan oprettes i app/web, men ikke via API.
- **Ingen prioritetsniveauer** — sortering er manuel (drag-and-drop). Brug position i listen som prioritet.

---

## Migration fra Trello

Vores Trello-board "Kris" har 5 lister:
- TransportIntra
- Rejsebureauet
- Arkitektur
- Personligt
- Done

**Plan:** Vi kan enten:
1. **Kopiere aktive tasks manuelt** — der er nok ikke mange åbne
2. **Script-migration** — Claude henter fra Trello API, opretter i Tasks

Trello-boardet beholdes som arkiv. Nye tasks → Google Tasks.

---

*Opdateret: 21. februar 2026*
