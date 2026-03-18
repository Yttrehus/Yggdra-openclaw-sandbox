# TransportIntra — Den Komplette Profil

**Version:** 3.0 (endelig)
**Dato:** 15. februar 2026
**Proces:** Skrevet → kritiseret → omskrevet → kritiseret → finaliseret

---

## Del 1: Mennesket

Kristoffer Yttrehus er 37 år, fra Aarhus. Han kører organisk affaldsrute 256 — en lastbil på 16-20 tons, 50-80 containere om dagen, 400+ om ugen. Han starter kl. 4 om morgenen og kører til han er færdig. 60 timer om ugen. 800.000 kr. om året. Ejer 40% af et rejsebureau. Bor alene.

Han ryger en pakke om dagen og er bange for at han spilder sit liv.

> "Jeg er 37. Bor alene. Jeg er lidt bange for at jeg spilder mit liv. Men hvis jeg nu bruger AI til at maksimere den tid jeg har tilbage. Så kan jeg måske indhente meget af det forsømte og få et godt liv."

Alt der kommer efter — appen, koden, visionen — er et forsøg på at bevæge sig fremad i stedet for at stå stille.

### Hvordan han tænker

Kris tænker i systemer. Hans hjerne forbinder koncepter via relationer, ikke via kategorier. Når han taler om humor, ender han ved videnskab. Når han taler om sin far, ender han ved empati vs. forståelse som filosofisk distinktion. En 45-minutters voice memo hopper mellem sorteringsalgoritmer, barndomstraumer, diesel-forbrug og den offentlige sektors pengestrømme — og det hænger alt sammen i hans hoved.

Han har en empati-motor der originalt var bygget til at overleve en barndom med usikre relationer. Den samme motor — evnen til at modellere andres mentale tilstande — bruger han nu til at modellere komplekse systemer. Det er den samme kognitive arkitektur.

Hans beslutningsproces: intuition først, logik derefter. Mavefølelsen er informationssignal, ikke støj. Men han har også en perfektionisme der lammer ham:

> "Hvis jeg ikke ved hvad det rigtige er at gøre, hvor jeg er sikker på at jeg ikke fortryder det, så gør jeg ikke noget overhovedet. Og så står jeg bare stille."

Indtil frustrationstærsklen overskrides. Da handler han med en intensitet der overgår de fleste.

### Tre lag af drivkraft

**Det eksistentielle:** Han vil have et liv der tæller. Han refererer til HER, TARS fra Interstellar, Jane fra Ender's Game — AI-ledsagere der *kender* deres menneske. Det er et designmål: en forlængelse af sig selv, ikke et værktøj.

**Builder-identiteten:** *"Tror du jeg vil abonnere på lorte-LLM'er resten af mit liv? Nej, jeg vil fine-tune min egen AI-model."* Han vil eje sine systemer, sit data, sin server. Afhængighed er tab af kontrol.

**Frustrationen:** Appen er dårlig. Den koster ham tid. Kontoret er ligeglad. *"Nu er jeg bare træt af det, så nu gør jeg det fandme selv."*

Disse tre lag forstærker hinanden. Frustrationen legitimerer byggeriet. Byggeriet skaber mening. Meningen trumfer perfektionismen.

### Hans læringsmodel

Karl Popper som byggeprincip:
> "Byg det så fedt og avanceret som muligt. Derefter kan det streamlines. Rinse and repeat."

Og:
> "Byg det i hovedet, kritisér det efterfølgende, byg bedre, afbureaukratisér så meget som muligt."

Han lærer ved at gøre, ikke ved at læse. Han starter med slutresultatet og arbejder baglæns. Han kæmper sig igennem fejl med en stædighed der grænser til besættelse. 777 beskeder i én samtale. 2.232 over 10 uger.

### Hans designsans

"Shadow & Gold" — mørkt tema med guld-accenter. Ikke tilfældigt. Det er mørkt fordi han starter kl. 4 om morgenen, hvor hvid baggrund blænder. Guld fordi det skal signalere kvalitet, ikke bare funktionalitet.

> "100% forståelse på 0.5 sekunder."

Han tænker visuelt. Mindmaps. Diagrammer. Han vil se kompleksitet reduceret til klarhed. Ikke som en designer der har studeret det — som en bruger der ved hvornår noget *føles* rigtigt.

---

## Del 2: Hvad TransportIntra er

webapp.transportintra.dk — et ruteadministrations-system til renovationsbranchen. Brugt af chauffører, disponenter og kontorfolk. En webapp med REST API. Den virker. Den er ikke smuk.

### Opbygning

```
Login → Menu → Listeside (ruter per dato) → Ruteoversigt (stop-listen)
                                            → Kort (Google Maps, knappenåle)
                                            → Vægtregistrering
         → Chat (kontor ↔ chauffør)
         → Tidsregistrering
         → Manuel ordreindtastning
```

### API'en

| Endpoint | Funktion | Begrænsning |
|----------|----------|-------------|
| `doLogin` | Session cookie | Udløber ved inaktivitet |
| `getDisps4Day` | Liste af ruter per dato | Ingen caching |
| `getRute` | Komplet rutedata (stop, GPS, containere, kommentarer) | Ingen diff — altid fuld download |
| `setPriority` | Ændr sorteringsnummer | Ét stop per kald. 400 stop = 400 kald. |
| `checkMail` | Heartbeat hvert minut | Tjekker KUN beskeder, IKKE nye stop |
| `kvitter`/`afvis`/`fejl` | Statusændringer | — |
| `setWeight` | Registrér vægt | — |

### Nøgledata fra getRute

Hvert stop indeholder: rute_id, disp_id (varierer ugentligt), adresse, GPS-koordinater, containertype(r) og antal, prioritet (sorteringsnummer), permanente kommentarer, vægt, status, og linjeposter.

`disp_id` ændrer sig fra uge til uge. `rute_id` kan variere per ugedag. Sorteringsnumre nulstilles for nye stop. Master opdateres kun manuelt af kontoret.

---

## Del 3: Frustrationerne — fra Kris' dagligdag

### 1. Søndags-ritualet (den der startede alt)

> "Ud af 400 stops, så er nok halvdelen af dem nuller eller ubrugelige. Hver søndag, hvis jeg vil have dem i en rigtig rækkefølge, skal jeg manuelt gå ind og trykke på det og taste ind. Det tager mig måske en time."

En time hver søndag. I to år. Han har klaget. Kontoret har svaret. Intet er sket. *"Sådan har det været i to år, og jeg har hele tiden sagt det."*

Da han løste det med N8n: 400 API-kald, 5 sekunder. Fra 1 time til 5 sekunder. Det var det øjeblik han forstod hvad der var muligt.

### 2. Navigations-bureaukratiet

> "Der er rigtig meget bureaukrati i sådan en simpel handling som bare lige hurtigt at kigge."

At tjekke morgendagens rute: ud → load → skift dag → load → vælg → load → se → tilbage → load → skift → load → vælg → load. **13 handlinger, 7 API-kald. For at kigge.**

### 3. Chat-problemet

> "Der er et lille chat-symbol der blinker. Men jeg kan ikke se hvad det er, medmindre jeg går ind i chatten. Og ofte er det en ligegyldig fælles-chat."

6+ handlinger for en besked der måske er irrelevant.

### 4. Ingen genopfriskning

`checkMail` kører hvert minut — men tjekker kun beskeder, ikke nye stop. Nye stop får nummer 0 og lander bagerst. Kris opdager dem først når han er færdig med sin rækkefølge. Ingen notifikation, ingen advarsel.

*"Det kunne være fint, hvis der var en lille pop-up-besked, om der er kommet noget nyt."*

### 5. Ingen caching

Hvert sideskift = nyt API-kald. Data den allerede har hentet, henter den igen. Ved dårlig forbindelse: "Serverfejl" → vent → prøv igen.

*"Hvis der nu kunne beholde de næste 5 dage og sidste 5 dage, så 10 dage i alt i cachen. Så den ikke skulle loade noget."*

### 6. Google Maps forstår ikke lastbiler

> "Google Maps antager at man kører i en personbil. Og der er rigtig mange steder hvor man ikke kan køre med lastbil. Man ender nogle gange med at køre ind i en blindgyde."

Ingen højdebegrænsninger. Ingen breddebegrænsninger. Ingen miljøzoner. Ingen tungvogns-tidsbegrænsninger. 16-20 tons behandlet som personbil.

### 7. Forældede stop-kommentarer

*"Nogle gange er det noget der engang var vigtigt, og så har det ændret sig. Men teksten læses ikke automatisk. Der skal jeg manuelt skrive ind til kontoret, om de ikke vil slette eller skrive noget andet. Og der er der ingen der gider."*

Kris planlægger efter information der er 6 måneder gammel. Kollegaer der kører hans rute arver samme forældede info.

### 8. Tidsregistrering og køretøjsskift

Kræver fuld sidenavigation. Kris glemte at skifte køretøj i to uger. *"Det kunne være fedt hvis man kunne gøre det uden egentlig at skulle loade nogle sider."*

### 9. Kollegaer som usynlige ressourcer

> "Jeg glemte en bestemt nøgle. Det ville koste mig en halv time at køre hjem og hente den. Men ved et held kom jeg i tanke om at en kollega kørte i nærheden. Jeg ringede, han kom forbi, og i stedet for en halv time brugte jeg to minutter."

Tilfælde. Held. Hvad med alle de gange det *ikke* skete?

### 10. Ingen vidensdeling

> "En kollega skulle til at stoppe. Så kørte han én dag med mig. Han har nu været der i 2 år."

Retention er 3 måneder typisk. Viden lever i hovedet på den enkelte chauffør og dør med ham. Intet system fanger den.

### 11. Vægtfunktionens quirks

Ændring af totalvægt trækker fra lasten i stedet for at opdatere basevægt. Knapper er svære at ramme fra lastbilen.

### 12. Hvid baggrund kl. 4

*"Appen er hvid baggrund og meget lysfarver, og jeg starter klokken 4 om morgenen, så er lyset rigtig skarpt."*

---

## Del 4: Hvad han har bygget — rejsen

### Uge 1-2 (december 2025): Opdagelsen

2. december. Kris kører lastbil og tester voice-chat med Claude for første gang.

> "I'm driving around for work, and I have some things that I need to do while driving. So instead of me actively doing them while driving, I can get you by voice to execute them."

Inden for dage er han i gang med n8n, webhooks og API-reverse-engineering. Han analyserer network requests i browseren, dekoder payloads, og kortlægger endpoints.

### Uge 3-4 (december): Kampen

235 beskeder i samtale 23. Google Sheets-integration, workflow-design, automatisk sortering. Sessions der udløber. Multipart form data der fejler. Cookie-forwarding der driller.

> "LÆES FUCKING DET TXT JEG SENDTE TIL DIG I STARTEN IGEN OG I FUCKING GEN INDTIL DU ER SIKKER OG SAA GOER DU DET LIGE ET PAR GANGE MERE."

### Uge 5-6 (dec-jan): Visionen tager form

> "Ok tid til deep research. Jeg vil lave en app, jeg kan tilføje alle mulige funktioner."

1:1 kopi af TransportIntra-webapp, derefter forbedring. AI-agent ("Trashy") der styrer workflows. Google Apps Script til kundesortering. Kalender-lookup med Unix timestamps.

> "Filosofien bag byggeprojektet er meget Karl Popper: byg det så fedt og avanceret som muligt. Derefter kan det streamlines. Rinse and repeat."

### Uge 7 (januar): Tabet

Alle n8n workflows forsvandt.

> "Har tilsyneladende mistet alle mine workflows på serveren. Du har tilfældigvis ikke nogle af dem her i historikken som JSON?"

Forsøg på at redde fra samtalehistorikken. Delvist succes. Men beslutningen er truffet: Claude Code i stedet for n8n.

### Uge 8-10 (januar-februar): Genopbygningen

Claude Code. Webapp-klon. Docker. Nginx. SSL. Qdrant. Telegram-bridge. Voice-API. Research-tools. 70.408 vektorer. 9 cron-jobs. Automatisk dagbog.

Fra 0 til produktionssystem på 10 uger. Uden kodningserfaring.

> "I am all in. Now or never."

### Hvad han kan nu, som han ikke kunne for 10 uger siden

- Reverse-engineer en REST API fra browser network requests
- Bygge og deploye en webapp (HTML/CSS/JS + Node.js)
- Konfigurere Docker containers, nginx reverse proxy, SSL
- Bruge git til versionering
- Sætte Qdrant op med embeddings og semantisk søgning
- Skrive Python scripts til automation og data-processing
- Administrere en Linux VPS via terminalen
- Forstå og implementere OAuth2-flows (Google, Microsoft)
- Bygge research-tools der søger i akademiske databaser

10 uger. Fra nul.

---

## Del 5: Det der er bygget nu

### Webapp-klonen

**Stack:** HTML/CSS/JS (vanilla) + Node.js (Express) + nginx/Traefik (SSL) + Qdrant
**Adresse:** https://app.srv1181537.hstgr.cloud
**Design:** "Shadow & Gold" — mørkt tema, guld-accenter, PWA-installérbar

**Implementeret:**
- Login med TransportIntra credentials (proxy)
- Ruteoversigt med alle stop, prioriteter, adresser, containere
- Lokal sortering (drag-and-drop + manuelle numre)
- Vægttracker med undo/redo
- Google Maps med knappenåle
- Chat-integration (Claude via Ydrasil)
- GPS-tracking
- Tidsregistrering
- Manuel ordreindtastning
- PWA-support (offline cache, installérbar)

**Ikke implementeret:**
- 10-dages caching
- Sorteringsprofiler (kl. 4 vs. kl. 6)
- Drop-down chat/tidsreg/køretøjsskift
- Personlige stop-noter
- Proaktiv genopfriskning (nye stop)
- Kollegaoverblik
- Lastbilnavigation
- Server-synkronisering af sorteringsnumre
- **Test med andre end Kris**

### Ydrasil-økosystemet

Appen voksede til et helt system:

| Komponent | Hvad det gør |
|-----------|-------------|
| Qdrant | 70.408 vektorer: rutedata, sessions, rådgiver-viden, voice memos |
| Cron-jobs (9 stk.) | Daglig backup, auto-dagbog, session logging, monitoring |
| Telegram-bridge | Kris → Claude via Telegram fra telefonen |
| Voice-API | Speech-to-text + LLM + text-to-speech |
| Research-tools | Søgning i arXiv, OpenAlex, Semantic Scholar |
| Brain/ | Intent, memory, retrieval (MISSION, playbooks, Qdrant config) |
| Integrationer | Gmail, Hotmail/Outlook, Google Calendar (Trello + Mindmap planlagt) |

---

## Del 6: Visionen

### 3 måneder: "Det der virker"

Appen klar til at en kollega kan bruge den. Præcist:

1. **Sortering der overlever** — aldrig mere søndags-ritual
2. **10-dages cache** — ingen unødvendige API-kald
3. **Pop-up notifikationer** — nye stop, chat, ændringer
4. **Drop-down alt** — chat, tidsreg, køretøj, kalender fra hovedskærmen
5. **Personlige noter** — per stop, lokale, delbare
6. **Profiler** — kl. 4-start, kl. 6-start, afløser-profil

### 6-12 måneder: "Assistenten"

> "At have en assistent i øret, der gør at jeg næsten aldrig har brug for at kigge på en skærm."

- **Morgen-briefing:** "Godmorgen Kris. 62 stop i dag. 3 nye. Regn fra kl. 10. Ny kunde på Søndervangsvej — lav port, parkér på gaden."
- **Kollegaoverblik:** Frivillig positionsdeling. Aldrig mere tilfældig nøgle-redning.
- **Stemme-registrering:** "Færdig." → Stop afsluttes. "20 kilo, 2 spande." → Logget.
- **Prædiktiv logistik:** Tidsestimat, tankningsforslag, fyldningsgrad.
- **Lastbilnavigation:** Kender højde, bredde, vægt. Ingen blindgyder.

### 1-3 år: "Platformen"

- Andre chauffører bruger appen
- 12 måneders data → automatisk ruteoptimering
- Onboarding: nye chauffører arver viden, ikke bare ruter
- Skalering til rejsebureauet

### Drømmen

> "Det ultimative drøm, det er at udvikle en personlig assistent, som nærmest forstår mig så godt, at man skulle tro at den var indopereret som chip i min hjerne. Så hvis den forstod alle mine tanker. Fik alt det data jeg nu har — alle de kommentarer og chats jeg har haft på Facebook igennem 10 år. Alt det jeg har skrevet eller sagt. Alt mit data fra mit ur, der tager min puls. Måske også data fra blodprøver. Psykologisk data. Så jo mere den ved, jo tættere og tættere kommer den på mig og kan hjælpe mig med at være mit kompas. Så jeg får mest muligt ud af livet."

TransportIntra er det første kapitel. Ikke det vigtigste. Men det der lærer ham at bygge.

---

## Del 7: Kulturen og gabet

TransportIntra er bygget af et firma der sælger til renovationsselskaber. Kris' arbejdsgiver betaler. Chaufførerne bruger det. Ingen af dem har indflydelse på udviklingen.

> "De gider ikke samle de der små wins. De har ingen forståelse for lastbilchaufførerne, ligesom vi ikke har forståelse for hvordan det er at sidde på kontoret. Vi lever i forskellige verdener."

> "Jeg har skrevet en række ændringer jeg gerne vil have lavet, og så siger de ja det skal jeg nok, og så får de det ikke gjort. De har travlt, og de løser kun problemer der er flest penge i. Eller problemer når det først brænder på."

**Konsekvensen:** Kris bygger sit eget system. Ikke oprør. Pragmatisme.

**Det bredere mønster:** Den samme dynamik eksisterer overalt. Brugere vs. udviklere. Chauffører vs. kontor. Borgere vs. myndigheder. Dem der oplever friktionen og dem der designer systemerne lever i forskellige virkeligheder.

Kris' dybeste ambition er at bygge broer. Først for sig selv (TransportIntra). Så for sine kollegaer (platformen). For sin veninde (bogføring). For sin ven (rejsebureauet). Til sidst for samfundet:

> "Jeg ser det som en programmeringsopgave. Hvad hvis man brugte den videnskabelige metode? Ligesom den der har fået os til at flyve. Vi kan få 100.000 tons stål med 200 mennesker ombord til at flyve, fordi man har brugt den videnskabelige metode. Og man har ikke skændtes og brugt følelser og personangreb."

Kortlæg pengestrømme. Find spild. Visualisér det. Ingen politisk side. Bare data.

Alt Kris gør handler om det samme: **tag noget uigennemskueligt, kortlæg det, fjern friktionen, gør det synligt.**

---

## Del 8: Fejlene og lektierne

### Tabet (januar 2026)

Alle n8n workflows forsvandt fra serveren. Ingen backup. Kris forsøgte at redde fra samtalehistorikken.

**Lektie:** Backup, backup, backup. Nu: daglig backup kl. 04:00 + Hostinger VPS backup + Qdrant snapshots.

### Agent-timeouts (3+ gange)

Research-agenter kørte 10-30 minutter uden feedback. Kris' tid spildt mens han ventede.

**Lektie:** Altid timeout. Altid feedback. Maks 3-5 minutter per agent.

### Discount-bias

Claude foreslog gentagne gange lettere versioner af Kris' vision. Eksempel: Kris beskrev et hierarkisk vidensindeks. Claude sagde "ambitiøst og dyrt" og foreslog en simpel classifier. LightRAG viser at Kris' arkitektur er realistisk, billig, og har 28.000 GitHub stars.

**Lektie:** Tag visionen seriøst. Forstå før du forenkler.

### Kontekst-overload

777 beskeder i én samtale. Kontekstvinduet fyldt. Vigtig information tabt.

**Kris' løsning:** Sessionsbaseret kontekst med automatisk komprimering. Dedikerede sessions per projekt. Automatisk dokumentation af alt.

### Aldrig testet

Appen har aldrig forladt Kris' tablet. Ingen kollegaer har prøvet den. Ingen brugerfeedback. 10 ugers arbejde valideret af kun én person.

---

## Del 9: Ærlig vurdering

### Hvad er realistisk

**Ja, inden for 3 måneder:**
- Fuldt funktionel app til Kris personligt (caching, sortering, drop-downs, noter)
- Test med 2-3 kollegaer
- Voice-briefing via eksisterende voice-API

**Ja, men kræver disciplin:**
- Sorteringsprofiler
- Server-synkronisering
- Rejsebureau-pilotprojekt

**Risikabelt:**
- Kollegaoverblik (kræver at andre bruger appen)
- Lastbilnavigation (kræver Google Maps Heavy Vehicle API eller egne data)
- Platform-skalering (kræver en backend Kris ikke ejer)

### De fem risici

1. **Scope creep.** Visionen vokser hurtigere end implementeringen. TransportIntra → videnssystem → livsoptimering → samfundsreform. Risikoen: intet bliver *færdigt*. Kris ved det selv — det er hans perfektionisme i ny forklædning.

2. **Afhængighed.** €180/måned til Anthropic. Hele systemet bygget med og omkring Claude. Kris vil eje sine egne systemer — men lige nu ejer han det modsatte.

3. **Uvalideret produkt.** 10 ugers arbejde. 70.408 vektorer. 0 brugere ud over Kris. Designvalg baseret på én persons intuition.

4. **API-sårbarhed.** TransportIntra kan ændre endpoints. Hele proxy-arkitekturen bryder sammen. Kris kan ikke forhindre det.

5. **Perfektionisme-cyklen.** Ydrasil har automatisk dagbog, 9 cron-jobs, research-tools, Telegram-bridge og Gmail-integration. Men appen er aldrig testet med en kollega. Infrastruktur der supporterer et produkt der ikke eksisterer som produkt.

### Den ene ting der tæller

**Få appen i hænderne på én kollega.**

Ikke fordi feedbacken er teknisk værdifuld. Men fordi det bryder cyklen. Det forvandler TransportIntra fra et laboratorium til et produkt. Det gør drømmen til noget der eksisterer uden for Kris' eget hoved.

Alt andet — voice-AI, kollegaoverblik, lastbilnavigation, rejsebureauet, bogføreren, samfundsprojektet — kommer efter den ene handling.

Kris sagde det selv:
> "Jeg planlægger og planlægger og planlægger og gør aldrig noget for jeg finder ikke den perfekte løsning."

Appen behøver ikke at være perfekt. Den behøver at blive *brugt*.

---

## Appendiks A: Frustrationsliste

| # | Frustration | Alvor | Status |
|---|------------|-------|--------|
| 1 | Ugentlig nulstilling af sorteringsnumre | Kritisk | Løst (lokal) |
| 2 | 13 handlinger for at se morgendagens rute | Høj | Design klar |
| 3 | Chat kræver fuld sidenavigation | Høj | Design klar |
| 4 | checkMail opdaterer ikke rutedata | Høj | Ikke implementeret |
| 5 | Ingen caching — genloader allerede hentet data | Høj | Ikke implementeret |
| 6 | Google Maps forstår ikke lastbiler | Middel | Langsigtet |
| 7 | Forældede stop-kommentarer | Middel | Design klar |
| 8 | Tidsreg/køretøjsskift kræver sidenavigation | Middel | Design klar |
| 9 | Ingen kollegaoverblik | Middel | Langsigtet |
| 10 | Vægtfunktionens UI og logik | Lav | Delvist løst |
| 11 | Hvid baggrund kl. 4 om morgenen | Lav | Løst (Shadow & Gold) |
| 12 | Ingen onboarding for nye chauffører | Lav | Langsigtet |

## Appendiks B: Nøgle-citater (kronologisk)

**2. dec 2025 — Dag 1:**
> "I'm driving around for work, and I have some things that I need to do while driving."

**11. dec 2025 — Visionen begynder:**
> "My plan is to set it all up so you will work perfectly and smoothly with me."

**13. dec 2025 — Frustrationens peak:**
> "LÆES FUCKING DET TXT JEG SENDTE TIL DIG I STARTEN IGEN OG I FUCKING GEN INDTIL DU ER SIKKER."

**20. dec 2025 — App-ideen:**
> "Ok tid til deep research. Jeg vil lave en app, jeg kan tilføje alle mulige funktioner."

**21. dec 2025 — Builder-identiteten:**
> "Tror du jeg vil abonnere på lorte-LLM'er resten af mit liv? Nej, jeg vil fine-tune min egen AI-model."

**Jan 2026 — Passionen:**
> "Ok, det er gået op for mig hvor omfattende det her projekt er og har fuld intention om at blive super effektiv. Har fundet lidt en passion for denne type AI-projekter."

**1. feb 2026 — Drømmen:**
> "Det ultimative drøm er at udvikle en personlig assistent som nærmest forstår mig så godt at man skulle tro at den var indopereret som chip i min hjerne."

**2. feb 2026 — Vendepunktet:**
> "Nu er jeg bare træt af det, så nu gør jeg det fandme selv."

**2. feb 2026 (aften) — All in:**
> "I am all in. Now or never."

## Appendiks C: Teknisk reference

### API-endpoints

| Endpoint | Input | Output | Note |
|----------|-------|--------|------|
| `doLogin` | brugernavn, password | session cookie | Udløber ved inaktivitet |
| `getDisps4Day` | dato | liste af ruter (id, navn, status) | — |
| `getRute` | rute_id, dato | fuld rutedata (stop, GPS, containere, prioriteter, kommentarer) | Ingen diff-mode |
| `setPriority` | disp_id, stop_id, nummer | success/fail | Ét stop per kald |
| `checkMail` | — | besked-status | Kun beskeder, ikke rutedata |
| `kvitter` | stop_id | success | Marker som afsluttet |
| `afvis` | stop_id, årsag | success | Marker som afvist |
| `setWeight` | stop_id, vægt | success | — |
| `doTidsReg` | type (ind/ud), tidspunkt | success | — |

### Kendt data-adfærd

- `disp_id` ændrer sig fra uge til uge (dynamisk tildeling)
- `rute_id` varierer per ugedag
- Sorteringsnumre for nye stop = 0 (nulstilles ugentligt)
- Ingen webhooks — kræver polling
- Ingen batch-endpoints — 400 stop = 400 kald
- `checkMail` returnerer ikke ændringer i rutedata

---

*Version 3.0 — 15. februar 2026.*
*Proces: Skrevet → kritiseret (10 mangler identificeret) → omskrevet → kritiseret (7 forbedringer) → finaliseret.*
*Kilder: 7 voice memos, 28 samtaler (2.232 beskeder), Claude.ai-eksport, webapp-kildekode, API-dumps, Google Drive-imports, session-logs, audit-rapporter.*
