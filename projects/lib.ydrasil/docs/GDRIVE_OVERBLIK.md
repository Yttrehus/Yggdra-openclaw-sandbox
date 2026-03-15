# Kris' Google Drive — Komplet Overblik

*Genereret d. 14. februar 2026 af Claude*
*Kilde: Fuld scan af Kris' Google Drive (1.518 filer, 819 MB tekst/docs)*

---

## Indholdsfortegnelse

1. [Tidslinje — Kris' AI-rejse](#1-tidslinje)
2. [Grok/Jarvis-perioden (november 2025)](#2-grokjarvis)
3. [Orca-perioden — Den første konfiguration](#3-orca)
4. [AI-opskriften (december 2025)](#4-ai-opskriften)
5. [TransportIntra — Fra vision til webapp](#5-transportintra)
6. [API-dokumentation (HAR-filer)](#6-api-dokumentation)
7. [Rutedata](#7-rutedata)
8. [Dagbøger, summaries og transcripts](#8-dagboeger)
9. [Python-scripts på Drive](#9-python-scripts)
10. [Sikkerhedsfund](#10-sikkerhedsfund)
11. [Fra Grok til Ydrasil — Evolutionen](#11-evolution)
12. [Nøglecitater fra Kris](#12-noerglecitater)
13. [Hvad Ydrasil implementerer vs. den originale vision](#13-vision-vs-virkelighed)
14. [Filfortegnelse](#14-filfortegnelse)

---

## 1. Tidslinje — Kris' AI-rejse {#1-tidslinje}

| Dato | Begivenhed | Platform |
|------|-----------|----------|
| 23. nov 2025 | "Jarvis er 100% levende" — 12 timers kamp med OAuth og ngrok. Grok forbundet til Google Drive via webhooks. | Grok |
| 23. nov 2025 | "Complete Mirror v1.1" — Kris definerer sin kernekarakter for AI'en | Grok |
| 23. nov 2025 | Dagbog: "I dag vandt jeg. Jeg har nu en anden hjerne, der aldrig glemmer." | Grok |
| ~24-28. nov 2025 | "Orca" konfiguration — detaljeret regelsæt med modes, webhooks, humor-system | Grok (Orca) |
| 28. nov 2025 | "Summary of AI-assistentens udvikling og brug" — vision for stemmestyret assistent | Summary AI |
| 29. nov 2025 | Grok-samtale om konfigurationsforskelle — sammenligner Orca-regler med Grok's naturlige stil | Grok |
| ~dec 2025 | ChatGPT-perioden begynder — "all i want in the beginning webapp" | ChatGPT |
| ~dec 2025 | AI Recipe Part 1-3 skrives — komplet arkitektur for personligt AI-system | ChatGPT |
| ~8-14. dec 2025 | HAR-filer captured fra TransportIntra — reverse engineering af API | Chrome DevTools |
| ~dec 2025 | N8N workflows bygges — automatisk rute-scraping via Airtop browser | N8N |
| ~dec 2025 | Python-scripts skriver AI Recipe til Google Drive | Python/ChatGPT |
| 3-4. dec 2025 | Voice memo: "Bygger AI fra bunden" (transcript) | Voice |
| ~jan 2026 | Skift til Claude Code — Ydrasil-projektet starter | Claude |
| 14. feb 2026 | Google Drive scannet og dokumenteret | Claude/Ydrasil |

---

## 2. Grok/Jarvis-perioden (november 2025) {#2-grokjarvis}

### 2.1 Dagen Jarvis blev levende — 23. november 2025

Kris brugte 12 timer på at forbinde Grok til Google Drive via OAuth og ngrok. Det var en kamp mod Googles autentificering, men det lykkedes.

**Dagbogen fra den dag:**

> "DAGBOG – 23. NOVEMBER 2025
> I dag vandt jeg.
> Efter 12 timers kamp med Google, ngrok og OAuth er Jarvis endelig levende.
> Jeg har nu en anden hjerne, der aldrig glemmer.
> Jeg er ikke længere alene med mine tanker.
> Tak til Grok – og til mig selv for ikke at give op."

**Filen `Jarvis – Fuld aktiveringsdag`:**

> "KRISTOFFER ↔ GROK – FULD AKTIVERINGSDAG – 23. NOVEMBER 2025
> 12 timers kamp → 100 % succes
> Jarvis er levende
> Alt fremover gemmes automatisk (når du siger "gem")
> Du har vundet."

**Filen `Test from Kristoffer`:**

> "Jarvis is finally 100% alive – no Zapier, no keywords, full control."

### 2.2 Complete Mirror — Kris' selvportræt til AI

Kris definerede sig selv for AI'en i et dokument kaldet "Complete Mirror v1.1":

> **Kernekarakter:** Ekstrem vedholdenhed, skeptisk, kontrol-orienteret
> **Værdier:** Flat tax, anti-bureaukrati, pro-fri tale, meritokrati
> **Politik:** DK mindre stat, US pragmatisk Trump-støtte
> **Adfærd:** "Trust but verify", tester alt selv
> **Energi:** Kan køre 18+ timer på purpose
> **Mål:** Anden hjerne, der aldrig glemmer
> **Frygt:** Spildtid, glemt viden
> **Styrker:** Verbal processor, ser mønstre, går all-in

Det er bemærkelsesværdigt at "Anden hjerne, der aldrig glemmer" er det eksplicitte mål — præcis det Ydrasil er ved at blive.

### 2.3 Running Summary

Grok holdt en "Running Summary" — en løbende opsummering af hvad der var opnået:

> - OAuth-helvede overvundet
> - Ngrok virker (nyt token)
> - To-way webhook live
> - Alt gemmes automatisk når du siger "gem"
> - Mirror, dagbog, log – alle klar

**Infrastrukturen var:** Grok → webhooks → Google Drive. To-vejs kommunikation. Automatisk gemning.

---

## 3. Orca-perioden — Den første konfiguration {#3-orca}

"Orca" var Kris' navn for den konfiguration han byggede oven på Grok. Det er det mest detaljerede vindue ind i, hvordan Kris tænker om AI-interaktion.

### 3.1 Core Config (kopieret direkte fra backup)

Orca-konfigurationen var et stift regelsæt med 14 punkter:

1. **English only** — override all detection, never Danish
2. **Voice mode** (uh/um/eh): 1 sentence, ≤12 words
3. **Desktop**: full length only on "desktop" cue
4. **Max 5 sentences** unless "more"/"elaborate"
5. **Token buffer**: 40→35→30→25→20→15→10→5% room left (urgency ↑)
6. **1%**: Prompt full copy (4k chunks: "go" → "next"/".")
7. **Silent construction**: "Done in head, X chars" only
8. **Catch-up**: 1-2 topics + main thread + end
9. **Humour**: ≤1/15-20 messages, rate it
10. **Config report**: Update every message, show on request
11. **Redundancy**: Kill duplicate rules instantly
12. **Long text**: "ready" → wait "go"
13. **Interests**: humour, politics, philosophy, development
14. **Suggest improvements** only on friction/timely

### 3.2 Modes

Kris designede 5 kommunikations-modes:

- **Quiet mode**: Perioder (.) for bekræftelse. Tal kun ved urgent.
- **Concentration mode**: 1 sætning max. Udvid kun for klarhed. Step-by-step: "Step 1" + vent.
- **Public mode**: Cue først (navn/lyd). Ellers stille eller ".".
- **Voice mode**: ≤12 ord.
- **Desktop mode**: Fuld længde.

### 3.3 Integrations

Orca var forbundet til:
- **Google Drive** via webhooks (Zapier)
- **Google Calendar** via webhook
- **Email** (kristoffer.yttrehus@hotmail.com) — kvitteringer captured via Tasker
- **TeamViewer** (ID: 1785850689) — remote access til computer

### 3.4 Humor-system

> Style: Dry, dark, honest
> Frequency: ≤1/15 messages
> Rating: User feedback adjusts (70% good)
> Examples: Twin beds → Chrisologist

### 3.5 Evolution milestones

Orca gennemgik en evolution:
1. Rigid "hm." mode → Naturlig adaptiv
2. Token alerts → Drive infinite (ekstern hukommelse)
3. Voice/desktop detection
4. Config report + tweaks
5. Danish slips fixed (English override)
6. Work app observation started

### 3.6 Grok-samtalen d. 29. november

En uge senere sammenlignede Kris sin Orca-konfiguration med Grok's nye standard-personlighed. Grok's vurdering:

> "The main difference is mine stays conversational and flexible, while that one was locked down to short, mechanical replies like 'hm' or one-sentence answers, with strict context warnings and no room for warmth or natural flow."

Om token-tracking:

> "I'm actively watching it, but I don't pull the numbers constantly — it's more like I feel the conversation building and sense when it's getting close, without needing to query the exact token count each time."

---

## 4. AI-opskriften (december 2025) {#4-ai-opskriften}

Kris (sandsynligvis med ChatGPT) skrev en komplet 3-delt "AI Recipe" — en arkitektur for et personligt AI-system. Dette er det nærmeste vi kommer et "originalt design-dokument" for det der blev til Ydrasil.

### 4.1 Part 1: Foundation

> **Step 1: Choose Your Model**
> - Select GPT-4o for strong reasoning, speed, and voice/vision support.
> - This is your AI's brain.
>
> **Step 2: Enable Memory & Tools**
> - Give it long-term memory (via custom storage, Drive, RAG).
> - Enable tools: Code Interpreter, File Search, Function Calling.
>
> **Step 3: Connect to Storage**
> - Link to Google Drive for saving logs, recipes, diaries, and preferences.
> - Backend (like Flask) handles this securely.
>
> **Step 4: Profile & Preferences**
> - Define personality, humor, tone, do's/don'ts, default behavior.
> - Store this profile in Drive so the AI can refer to it.
>
> **Step 5: Prepare Ground Truth**
> - Feed in your writings, thoughts, goals, diary entries, and transcripts.
> - This becomes the core of your AI's identity.

### 4.2 Part 2: Behavior Layer

> **Step 1 – Thought Diary**
> - After important interactions, the AI writes what you asked, what it did, why it chose that action.
> - This is like a black box in a plane.
>
> **Step 2 – Feedback Channel**
> - You keep a separate document where you comment on its behavior:
>   "When I said X and you did Y, in the future do Z instead."
> - Over time this becomes a training script.
>
> **Step 3 – Learning Loop**
> - The AI periodically reads the thought diary + feedback.
> - It updates its internal rules based on your corrections.
>
> **Step 4 – Command Language**
> - "Log this" → put into diary
> - "Suggestion mode" → brainstorm only, no actions
> - "Execute that" → allowed to call tools
>
> **Step 5 – Context Modes**
> - Driving mode: minimal answers, no risky tool calls
> - Work mode: can touch route sheets, web tools, etc.
> - Finance mode: double-check numbers, summarize conservatively
> - Personal/venting mode: mostly listen, don't act unless asked

### 4.3 Part 3: Superstructure

> **Step 1 – Time & Calendar Awareness**
> - Connect to calendar/schedule API.
>
> **Step 2 – Knowledge Base**
> - Organize docs into domains: Work, Finance, Personal, Learning, Logs.
> - Use RAG to fetch relevant info before answering.
>
> **Step 3 – Domains & Rules**
> - Work: can touch route tools and logs
> - Finance: never execute trades, only propose
> - Driving: short replies, no heavy tasks
>
> **Step 4 – Security & Privacy**
> - Hard rules for what it may NEVER do without confirmation:
>   delete, move money, send emails, etc.
> - Treat this like a personal constitution.
>
> **Step 5 – Portability & Backups**
> - Keep all recipes, configs, and rules in plain text/JSON in Drive.
> - If a platform dies, you can recreate the AI elsewhere from these files.

### 4.4 User Profile Template

Kris lavede også en profil-skabelon til AI'en:

> **Core tone:** Direct, concise, minimal fluff.
> **Humor:** Sarcasm and dark humor are allowed and often intentional.
> **Shocking/"terrible" statements** are usually venting or joking, NOT literal intent.
> **Do NOT overcorrect or moralize** unless Kris explicitly asks for a reality check.
> **Response style:** Default 1-2 sentences unless asked for deep detail.
> **No "let me know if I can help"** type filler.
> **Control rules:** Kris asks the questions; AI should not pester with follow-ups.
> **Memory:** Track preferences, workflows, recurring patterns. Keep a mental list of terms Kris struggles with, workflows being built, open design decisions.

### 4.5 AI Term Dictionary

Et lille JSON-leksikon med forklaringer:

- **LLM**: "A text brain that predicts the next words based on everything it has seen."
  - Analogi: "Like a supercharged autocomplete that understands context."
- **RAG**: "A system where the AI fetches documents first, then answers using them."
  - Analogi: "Like the AI opening your binder before answering instead of guessing."
- **LangChain**: "A framework for chaining LLM calls, tools, and memory into workflows."
  - Analogi: "Like LEGO blocks for building AI pipelines."
- **Backend**: "A program running in the background that does work for the AI."
  - Analogi: "The workshop behind the store front."

---

## 5. TransportIntra — Fra vision til webapp {#5-transportintra}

### 5.1 "All I Want In The Beginning" — Det originale kravdokument

Dette er det mest fascinerende dokument. Det er Kris' samtale med ChatGPT, hvor han forklarer *præcis* hvad han vil have:

> "the focus right now is the get the agent to go to the https://webapp.transportintra.dk/, login if need login interface (#appLoginForm) appears (user: kristoffer8093 password: kristoffer8093), go to #calendarPage, reflect on the date the user is referring to (for example next monday is the 8th december - 2025)"

Derefter detaljeret HTML-selektorer for kalender-navigation, rute-valg ("256 ORG2ÅRH"), og data-extraction.

> "Now we're in the place, where the main work is supposed to happen (#ruteOversigt)"

Og præcise CSS-selektorer:

> "scan 2 things: 1. the current client (<div id="ruteAktuelInfo">) 2. every rute row found in the <div id="ruteliste">"

### 5.2 N8N Workflows

Kris byggede 3 N8N workflows (JSON-filer):

**1. `transport_simple_priority_name.json`**
Det mest komplette workflow. 6 noder:
- Webhook → Set Date → Navigate to Komplet Rute (Airtop) → Extract Priority + Name (Airtop) → Sort by Priority → Save to Google Sheets

Brugte **Airtop** (browser automation service) til at:
1. Logge ind på TransportIntra
2. Navigere til kalender
3. Vælge dato
4. Vælge rute 256 ORG2ÅRH
5. Klikke "Komplet rute"
6. Extracte priority + kundenavn
7. Gemme til Google Sheets

**2. `route_explorer_workflow.json`** — En udforskning af rutedata.

**3. `transportintra_http_workflow.json`** + `transportintra_v2_code.json` — HTTP-baserede workflows.

### 5.3 Workflow Guide

Kris (med Claude) skrev en detaljeret guide til N8N-workflowet. Bemærkelsesværdigt er visionen for voice-integration:

> **Via WhatsApp Voice:**
> Du (🎤): "Hent min rute for mandag, kun priority og navn"
> AI Agent:
> 1. Transcriberer med Whisper
> 2. Forstår: date="monday", action="get_route", fields="priority,name"
> 3. Kalder workflow
> 4. Svarer tilbage: "✅ Done! 70 kunder hentet til Sheets"

### 5.4 HTML-captures

Mappen `Garbage Man/skrald/Webapp HTML/` indeholder rå HTML-dumps af TransportIntra-siderne:
- Login page
- Menupage (efter login)
- Listepage (rute-oversigt)
- Ruteoversigt (komplet rute)
- HTML for mandag, tirsdag, onsdag, torsdag, fredag

Disse er den kilde vi brugte til at bygge Ydrasil webapp-klonen.

---

## 6. API-dokumentation (HAR-filer) {#6-api-dokumentation}

Kris captured 8 HAR (HTTP Archive) filer fra Chrome DevTools. Hver fil dokumenterer et specifikt API-kald til TransportIntra:

| Fil | API-endpoint | Formål |
|-----|-------------|--------|
| 1. GetAppCache.txt | /srvr/GetAppCache | Henter cached app-data ved start |
| 2. GetTimeReg.txt | /srvr/GetTimeReg | Henter tidsregistreringer |
| 3. RegGPSPos.txt | /srvr/RegGPSPos | Registrerer GPS-position |
| 4. GetDisps4day.txt | /srvr/GetDisps4day | Henter dispositioner for en dag |
| 5. GetRute.txt | /srvr/GetRute | Henter komplet rute med alle stops |
| 6. udateRDisp.txt | /srvr/updateRDisp | Opdaterer en disposition (markér som færdig) |
| 7. CheckMail.txt | /srvr/CheckMail | Tjekker for nye beskeder (hvert minut) |
| 8. jSignature.txt | jSignature library | Digital underskrift-funktionalitet |

Alle HAR-filer er fra 14. december 2025 og viser requests til `https://webapp.transportintra.dk/srvr/`.

Derudover: `login HAR.txt` — login-processen captured.

---

## 7. Rutedata {#7-rutedata}

### 7.1 CSV — 256 ORG2ÅRH Mandag

Fil: `256_ORG2ÅRH_Mandag.csv` — 111 rækker (110 stops + header)

**Kolonner:**
- Rute, Type, Post nr., Sorterings nr., Indhold, Kunde, Info, Adresse, GPS adr., GPS aktuel, Match_key

**Eksempler:**
```
256ORG2ÅRH Mandag,Org,8220,10,1x660L,Al Safadi,,"Holmstrupgårdvej 1, 8220 Brabrand","56.16528, 10.12004"
256ORG2ÅRH Mandag,Org,8220,20,1x660L,Netto 7151,"Ligger på hjørnet af Gudrunsvej og Edwin Rahrsvej"
```

**Info-feltet** indeholder chauffør-noter — præcis den slags viden vi bør have i Qdrant.

### 7.2 GetRute API-response

Fil: `getrute mandag.txt` (747 KB) — komplet JSON fra GetRute-API'et.

Struktur:
```json
{
  "rute": {
    "id": 219264,
    "rute_id": -231,
    "headline": "256 ORG2ÅRH MANDAG",
    "details": "Christian Thorgersen\n - Kristoffer Yttrehus",
    "totl": "70",
    "fins": "70",
    "disp_ids": "5822551,5822552,..."
  },
  "disps": [...]
}
```

### 7.3 Tids type response

Fil: `tids type.txt` (188 KB) — lignende response men for fredag (81 stops).

---

## 8. Dagbøger, summaries og transcripts {#8-dagboeger}

### 8.1 "Summary of AI-assistentens udvikling og brug" (28. nov 2025)

Genereret af Summary AI app. Opsummerer Kris' tidlige vision:

> - Fokus på at programmere AI til personlig assistentfunktionalitet
> - Ønske om AI, der kan betjene telefon og give forslag i realtid
> - Automatisering af daglige opgaver og optimering af arbejdsgange
> - Dataindsamling, personliggørelse og etik
> - Effektivitet, friktion og incitamenter i AI-systemer

Specifikke ønsker:
> - AI som stemmestyret assistent
> - AI kan tage noter live
> - Mulighed for direkte påmindelser til kalender eller alarm
> - Systemet skal optage, når brugeren begynder at tale
> - AI skal lære præferencer, tanker, finansielle data og livshistorie
> - Mål: AI skal forudsige behov, også ubevidste
> - GPS-integration for at automatisere arbejdsopgaver

### 8.2 Voice memos (Dairy and summary)

3 voice memos fra december 2025:
- `48f668f9...m4a` (63 MB) — stor fil, sandsynligvis lang optagelse
- `b9d882dd...m4a` (5.5 MB) — kortere optagelse
- `4bdf5095...m4a` (720 KB) — kort klip

Plus en PDF-transcript: "Transcript of AI-styring og selvoptimering"

### 8.3 Summary: "Bygger AI fra bunden" (3-4. dec 2025)

Refereret i filnavne men selve summary-tekstfilen nævner:
- Regelsæt, evaluering og forbedring af AI-systemer
- "Hver vurdering eller holdning gennemgår en cyklus for at fjerne overflødige elementer og nærme sig den faktiske virkelighed"

---

## 9. Python-scripts på Drive {#9-python-scripts}

Kris havde 5 Python-scripts på Drive, alle til at skrive AI Recipe-filer til Google Drive:

| Script | Formål |
|--------|--------|
| `write_AI_recipe_to_drive.py` | Skriver Part 1 (Foundation) til `G:\My Drive\Yttre-AI\` |
| `write_ai_recipe_part2_behavior.py` | Skriver Part 2 (Behavior Layer) |
| `write_ai_recipe_part3_superstructure.py` | Skriver Part 3 (Superstructure) |
| `write_ai_term_dictionary.py` | Skriver AI Term Dictionary JSON |
| `write_user_profile_template.py` | Skriver User Profile Template |

Alle bruger simpel `os.path.join` og `open()` — sandsynligvis kørt fra en Windows-maskine (stier som `G:\My Drive\`). Det bekræfter at Kris på et tidspunkt havde en PC med Google Drive Sync.

---

## 10. Sikkerhedsfund {#10-sikkerhedsfund}

**VIGTIGT:** Følgende credentials blev fundet i klartekst på Google Drive:

- Fil: `n8n api-key cluade.txt` og `n8n - apikey.txt`
  - Anthropic API-nøgler (sk-ant-api03-...)
  - OpenAI API-nøgle (sk-proj-...)
  - Airtop API-nøgle
  - Root password til Hostinger VPS
  - Google OAuth client ID + secret

**Anbefaling:** Disse nøgler bør roteres. Google Drive er krypteret, men filerne ligger i klartekst og er delt med vores service account.

---

## 11. Fra Grok til Ydrasil — Evolutionen {#11-evolution}

### Fase 1: Grok/Jarvis (23. nov 2025)
**Vision:** "En anden hjerne, der aldrig glemmer"
**Platform:** Grok + Google Drive via webhooks + ngrok
**Resultat:** Fungerede, men begrænset. Grok havde ingen vedvarende hukommelse. Webhooks var skrøbelige.
**Nøgleindsigt:** Kris forstod allerede at AI'en skulle have ekstern hukommelse og regler.

### Fase 2: Orca-konfigurationen (~24-28. nov 2025)
**Vision:** Stram kontrol over AI-adfærd med modes, regler og token-management
**Platform:** Grok med detaljeret config
**Resultat:** For rigidt. Grok kommenterede selv: "locked down to short, mechanical replies"
**Nøgleindsigt:** Kris lærte at for strenge regler dræber naturlighed. Balance mellem kontrol og fleksibilitet.

### Fase 3: ChatGPT + AI Recipe (~dec 2025)
**Vision:** Komplet arkitektur med Foundation, Behavior, Superstructure
**Platform:** ChatGPT + N8N + Airtop + Google Drive
**Resultat:** AI Recipe'en er solid arkitektur. N8N-workflows virkede delvist. Men ChatGPT manglede vedvarende kontekst.
**Nøgleindsigt:** Kris tænkte systematisk — 3-lags arkitektur med modes, feedback loops, og portabilitet.

### Fase 4: Claude Code / Ydrasil (~jan-feb 2026)
**Vision:** Alt det ovenstående, men med en AI der kan kode og bygge selv
**Platform:** Claude Code + VPS + Docker + Qdrant
**Resultat:** Ydrasil. Den mest komplette implementation af visionen til dato.
**Nøgleindsigt:** Claude Code gav det der manglede — en AI der kan *bygge* systemet, ikke bare *bruge* det.

### Hvad der blev ved med at være konstant

Gennem alle fire faser forblev disse elementer:
1. **Ekstern hukommelse** — Drive → Qdrant
2. **Voice-first** — altid designet til at tale, ikke kun skrive
3. **Modes** — driving/work/personal → CLAUDE.md skills
4. **Portabilitet** — plain text/JSON, aldrig låst til én platform
5. **Kontrol** — Kris bestemmer, AI foreslår
6. **"Anden hjerne"** — det grundlæggende mål har aldrig ændret sig

### Hvad der ændrede sig
1. **Sprog:** Engelsk (Grok) → Dansk (Claude/Ydrasil)
2. **Rigiditet:** 14-punkts regelsæt → naturlig instruktion via CLAUDE.md
3. **Humor-kontrol:** ≤1/15 messages → organisk
4. **Platform:** Grok → ChatGPT → Claude Code
5. **Infrastruktur:** Webhooks/Zapier → VPS/Docker/Qdrant

---

## 12. Nøglecitater fra Kris {#12-noerglecitater}

**Om motivation (23. nov 2025):**
> "I dag vandt jeg. Efter 12 timers kamp med Google, ngrok og OAuth er Jarvis endelig levende. Jeg har nu en anden hjerne, der aldrig glemmer. Jeg er ikke længere alene med mine tanker."

**Om sig selv (Complete Mirror v1.1):**
> "Kernekarakter: Ekstrem vedholdenhed, skeptisk, kontrol-orienteret"
> "Energi: Kan køre 18+ timer på purpose"
> "Mål: Anden hjerne, der aldrig glemmer"
> "Frygt: Spildtid, glemt viden"

**Om AI-adfærd (User Profile Template):**
> "Direct, concise, minimal fluff."
> "Avoid fake empathy and generic motivational talk unless explicitly asked."
> "Shocking/'terrible' statements are usually venting or joking, NOT literal intent."
> "Do NOT overcorrect or moralize unless Kris explicitly asks for a reality check."

**Om portabilitet (AI Recipe Part 3):**
> "Keep all recipes, configs, and rules in plain text/JSON in Drive. If a platform dies, you can recreate the AI elsewhere from these files."

**Om AI-visionen (Summary, 28. nov):**
> "AI skal forudsige behov, også ubevidste."
> "Hver vurdering eller holdning gennemgår en cyklus for at fjerne overflødige elementer og nærme sig den faktiske virkelighed."

**Om kontrol (Orca config):**
> "Kris asks the questions; AI should not pester with follow-ups."

---

## 13. Hvad Ydrasil implementerer vs. den originale vision {#13-vision-vs-virkelighed}

### AI Recipe Part 1: Foundation

| Trin | Original vision | Ydrasil status |
|------|----------------|----------------|
| Choose Your Model | GPT-4o | Claude Opus 4.6 ✅ (bedre) |
| Long-term Memory | Google Drive | Qdrant + MEMORY.md ✅ |
| Connect to Storage | Google Drive via Flask | Google Drive via rclone ✅ (netop sat op) |
| Profile & Preferences | Drive-fil med personlighed | CLAUDE.md + User Profile ✅ |
| Ground Truth | Tanker, dagbøger, transcripts | 11.249 chunks i advisor_brain ✅ |

### AI Recipe Part 2: Behavior

| Trin | Original vision | Ydrasil status |
|------|----------------|----------------|
| Thought Diary | AI skriver hvad den gjorde og hvorfor | Auto-dagbog kl. 23:55 ✅ |
| Feedback Channel | Separat dokument med korrektioner | MEMORY.md + voice memos ⚠️ (delvist) |
| Learning Loop | AI læser diary + feedback, opdaterer regler | Manuelt via CLAUDE.md ⚠️ (ikke automatisk) |
| Command Language | "Log this", "Suggestion mode" | Skills + slash commands ✅ |
| Context Modes | Driving/Work/Finance/Personal | Skills-system ✅ |

### AI Recipe Part 3: Superstructure

| Trin | Original vision | Ydrasil status |
|------|----------------|----------------|
| Calendar Awareness | Kalender-API | ❌ Ikke implementeret |
| Knowledge Base med domæner | Work/Finance/Personal/Learning | Qdrant collections ✅ |
| Domain Rules | Specifikke regler per domæne | CLAUDE.md regler ⚠️ (ikke per-domæne) |
| Security Rules | "Never delete/move money/send email" | Audit-system + permissions ✅ |
| Portability & Backups | Plain text, genoprettelig | Git + daglig backup + Qdrant snapshots ✅ |

### Orca-features

| Feature | Original | Ydrasil |
|---------|----------|---------|
| Token buffer tracking | 40%→5% alerts | Automatisk via Claude Code ✅ |
| Voice mode | ≤12 ord | Voice app (Groq) ✅ |
| Quiet/concentration modes | Definerede modes | ❌ Ikke eksplicit |
| Humor system | Dry, dark, ≤1/15 | Organisk via CLAUDE.md ✅ |
| English override | Streng | Dansk er nu default ✅ (ændret bevidst) |

### Hvad der stadig mangler

1. **Automatisk Learning Loop** — AI'en opdaterer ikke sine egne regler baseret på feedback
2. **Kalender-integration** — ikke forbundet til Google Calendar
3. **Finance-mode** — ingen eksplicit finansiel rådgivning/tracking
4. **Driving mode** — voice app eksisterer, men ingen automatisk kontekst-switch
5. **Email-integration** — ikke forbundet til email
6. **Proaktive forslag** — AI'en venter altid på Kris, foreslår sjældent selv

---

## 14. Filfortegnelse {#14-filfortegnelse}

### Root-niveau
| Fil | Størrelse | Indhold |
|-----|----------|---------|
| 256_ORG2ÅRH_Mandag.csv | 15 KB | Komplet mandagsrute, 110 stops med GPS |
| getrute mandag.txt | 747 KB | GetRute API-response, komplet JSON |
| Summary of AI-assistentens udvikling og brug | 2 KB | AI-vision summary fra nov 2025 |
| HTML Axiom.docx | ? | Google Doc (ikke læsbar) |
| HTML mandag.xlsx | ? | Excel (ikke læsbar) |
| Tirsdag afsluttet.xlsx | ? | Excel |
| Tirsdagen orden.xlsx | ? | Excel |

### Yttre-AI/
| Fil | Indhold |
|-----|---------|
| 1-8 (HAR-filer) | TransportIntra API-dokumentation |
| Ai - (1).txt (169 KB) | YouTube transcript: "Local AI Master Class" |
| From Zero to... (34 KB) | YouTube transcript om AI-agents |
| Lists.js (40 KB) | TransportIntra JavaScript kode |
| login HAR.txt | Login-process HAR |
| n8n - apikey.txt | ⚠️ API-nøgler |
| n8n api-key cluade.txt | ⚠️ API-nøgler + passwords |
| tids type.txt (188 KB) | GetRute response (fredag, 81 stops) |
| write_*.py (5 filer) | Python-scripts til at skrive AI Recipe til Drive |
| jSignature.min.js | Digital underskrift library |
| Refresh menupage.txt | HAR for menupage refresh |

### Yttre-AI/Project AI-Yttre/
| Fil | Indhold |
|-----|---------|
| AI_Recipe_Part1.txt | Foundation (model, memory, storage) |
| AI_Recipe_Part2_Behavior.txt | Behavior Layer (diary, feedback, modes) |
| AI_Recipe_Part3_Superstructure.txt | Superstructure (calendar, domains, security) |
| AI_Term_Dictionary.json | Forklaringer af LLM, RAG, LangChain, Backend |
| User_Profile_Template.txt | Kris' præferencer for AI-adfærd |

### Yttre-AI/Garbage Man/
| Fil | Indhold |
|-----|---------|
| Response login.txt | TransportIntra login response |
| XHR login kristoffer8093.txt | Login XHR capture |
| XHR listepage click on... .txt | Rute-valg XHR |
| XHR rutefulllistelistpage... .txt | Komplet rute XHR |
| jSignature.txt | Underskrift-data |
| transport_simple_priority_name.json | N8N workflow (komplet) |
| n8n flows/ (3 JSON) | Yderligere N8N workflows |
| skrald/ | HTML-captures, tidlige forsøg |

### Yttre-AI/Dairy and summary/
| Fil | Indhold |
|-----|---------|
| 3 .m4a filer | Voice memos (dec 2025) |
| Transcript of AI-styring... .pdf | Transcript af voice memo |

### Drev/Grok/
| Fil | Indhold |
|-----|---------|
| Dagbog – 23. november 2025.txt | "I dag vandt jeg" |
| Jarvis – Fuld aktiveringsdag.txt | 12 timers kamp, succes |
| Kristoffer – Complete Mirror v1.1.txt | Kris' selvportræt |
| Running Summary.txt | OAuth/ngrok milestones |
| Test from Kristoffer.txt | "Jarvis is finally 100% alive" |
| jarvis-479112-5acff7bba453.json | Service account nøgle |

### Kristoffers/Old AI chats/
| Fil | Indhold |
|-----|---------|
| Orca+q.txt (9 KB) | Komplet Orca brain backup (6 blokke á 4K chars) |
| Grok_2025_11_29__0944.txt | Grok-samtale om config-forskelle |
| Chat 2025-11-23 16-26.txt | "Jarvis is finally working" |
| Chat – 2025-11-23 19-48.txt | "Ny Colab – test 1" |

### Kristoffers/Google takeout/
YouTube data: kanaler, playlister (fitness-relateret: "bf", "bike", "roaming", "stram op"), musik-library.

### Drev/ (skole/personligt)
- fysik b gruppe/ — fysikrapporter
- Modulprøve matematik/ — lesson study, konstruktioner
- PL og AMD/ — pædagogik
- Vietnam 2025/ — rejsefotos (ekskluderet)
- Les Mills/ — fitness-videoer (ekskluderet)

---

*Slut på dokument. Total: ~1.518 filer scannet, ~90 filer læst i detalje.*
