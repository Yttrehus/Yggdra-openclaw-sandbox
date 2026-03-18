# TransportIntra — Kronologisk Narrativ

Fra frustration over en ubrugelig webapp til et komplet alternativt system. Dec 2025 — mar 2026.

---

## Fase 1: Vision + reverse-engineering (dec 2025)

Grundproblemet var simpelt: webapp.transportintra.dk viser kunder i tilfældig rækkefølge. Hver morgen sorterer chaufføren manuelt via numre — et system designet til 1990'erne. Kristoffer ville automatisere det.

**2. december** definerede han projektet som "Route Management Automation" — et Axiom-baseret RPA-script der sorterer kunder automatisk. Planen: script → Zapier-integration. Simpelt nok, troede han.

**6. december** faldt det hele fra hinanden. En hel dag med MCP/Puppeteer endte i ren frustration. Ingen af browser-automation-værktøjerne virkede pålideligt med TI's webapp. Samme dag opdagede han n8n — og det blev vendepunktet. Parallelt begyndte Grok at kortlægge webapp-strukturen: login, menu, ruteoversigt.

**11. december** virkede den første pipeline: n8n + Airtop + Google Sheets. Den hentede prioritetsnumre og kundenavne fra TI og synkroniserede til Sheets. For første gang var data tilgængelig udenfor den lukkede webapp.

**13. december** kom den længste session — en debugging-marathon. n8n workflows til scanning, sortering, og Sheets↔TI API synk. Her dukkede idéen om en "selvlærende rutedatabase" op. Gentagende fejlmønstre blev dokumenteret, og samtalen bevægede sig mod en agent-arkitektur.

**14. december** afkodede Kristoffer API-responsen fra getRute: Unix timestamps, ordrestruktur, disp_id vs rute_id. Dette blev fundamentet for al senere API-arbejde. Uden denne forståelse var resten umuligt.

**21. december** skete det næste mentale skift. SQL blev fravalgt ("Sheets + API er nok"), men vigtigere: n8n's begrænsninger begyndte at frustrere. Kristoffer opdagede Claude Code og bemærkede: "rigtige apps" — ikke workflows, men kode. Frøet til webapp-klonen var plantet.

**Kausal kæde 1: Platform-evolution**
Axiom/Zapier (2/12) → Puppeteer fejler (6/12) → n8n virker (11/12) → n8n frustrerer (21/12) → Claude Code opdaget (21/12) → webapp-klon (feb 2026).
Hver platform-skift var drevet af konkret frustration, ikke teknologisk nysgerrighed. Kristoffer ville have ét: sorterede kunder.

---

## Fase 2: n8n raffinering + frustration (jan 2026)

Januar var en overgangsperiode. n8n virkede, men krævede konstant vedligeholdelse.

**3. januar** raffinerede han sorteringslogikken: sorteringsnr 0 = ny/ukendt kunde, behold getRute-værdien. En nested AI-agent kaldet "Trashy" blev bygget i n8n. Kristoffer krævede kodeændringer, ikke JSON-dumps — et signal om at n8n's visuelt-først-paradigme ikke passede hans arbejdsform.

**4. januar** planlagde han en database til rutedata: ~70 kunder/dag, 5 dage/uge. JSON fra getRute blev analyseret systematisk. Langsigtet dataindsamling via n8n-automation blev planlagt, men aldrig skaleret.

**18. januar** gik Claude Code + n8n i stykker. API keys, netværksproblemer, Sheets-automation fejlede. Sessionen markerede overgangen: n8n som primært værktøj var slut. Claude Code begyndte at overtage som supplement — og snart som erstatning.

**29. januar** dikterede Kristoffer app-bugs via Grok: kunder afsluttes med 0 kg, problemer ved to ruter. Dette var den første systematiske fejldokumentation — input til det der senere blev kompendiet.

**Kausal kæde 2: Fra kodeekspert til dokumentationssystem**
API-response afkodet (14/12) → bug-dokumentation (29/1) → API reference (feb) → kompendium v1-v5 (18-19/2) → kildeindex (mar 2026).
Hvert skridt byggede på det forrige. Uden getRute-afkodningen i december var API-referencen umulig. Uden API-referencen var kompendiet overfladisk.

---

## Fase 3: Webapp-klon + kompendium (feb 2026)

Februar var gennembrudsmåneden. To parallelle spor konvergerede: en lokal webapp og et professionelt kompendium.

**8. februar** var arkitektur-dag. Kristoffer designede en Telegram-bot med fuld TI-kontekst og diskuterede multi-universe arkitektur: separate repos per projekt. Beslutningen blev "hold alt i mono-repo nu, split via git subtree når det giver mening." Multi-universe blev aldrig implementeret, men principperne — isolation, kontekst per projekt — lever videre i den nuværende projects/-struktur.

**11. februar** blev webapp-klonen kortlagt på 30 minutter. Webapp'en tog form: en lokal klon af TI's funktionalitet, men med Kristoffers forbedringer oveni.

**14. februar** blev RAG-systemet opsat. API-referencen blev embeddet i Qdrant, så fremtidige sessioner kunne søge i TI-dokumentation. Et stille men kritisk infrastruktur-skridt.

**15. februar** eksploderede organiserings-ambitionerne. Trello-board "Ydrasil" med lister per projekt. TI-underprojekter identificeret: Navigation, Chat, Design, Research. En interaktiv mindmap-webapp (Cytoscape.js) blev bygget men parkeret pga. proxy-issues. Kristoffer sagde: "dette bliver vores mindmap indtil videre" om Trello.

**18. februar** blev kompendium v2 leveret: 117 KB, 12 kapitler, 4 SVG-diagrammer. Sort/hvid, Georgia serif — professionelt layout. Kristoffers reaktion: "Det her er et skridt i den rigtige retning. Det er det, jeg mener, når det skal være professionelt."

**19. februar** kom detaljeret feedback via ~20 min voice memo. Punkt-for-punkt gennemgang: adskil original vs. tilføjet per kapitel, flere screenshots, mere dybde (HTML-struktur, payloads), getRute historik tilbage til sept 2023, og JSON-format > PDF for LLM-forbrug. Inspiration fra Nate Jones: "falsk kode" som format.

**21. februar** overtog Google Tasks fra Trello. Widget på telefon var killer-feature. TI-Project blev tungeste board med 19 tasks. Organiserings-systemet skiftede for tredje gang (Trello ét board → Trello flere boards → Google Tasks).

**Kausal kæde 3: Sortering — fra manuelt til automatiseret**
Tilfældig kunderækkefølge (2/12) → n8n sorterer via Sheets (13/12) → nr 0 = ny kunde (3/1) → drag+drop i lokal webapp (feb).
Det der startede som et automatiseringsproblem endte som et helt nyt produkt. n8n-sorteringen var et stepping stone, ikke en løsning.

---

## Fase 4: Sterilisering + venter på PC (mar 2026)

Arbejdet skiftede karakter. Fra build til organiser.

**27. februar** verificerede Claude API-adgang til TI og fandt JS chaufførhåndbogen. Teknisk fundament bekræftet.

**Marts 2026** handlede om projekt-organisering. TI fik sin plads i projects/transport/. Sterilisering af kode og data. Tre prioriteter defineret for næste fase:
1. **Stop-beskrivelser** — voice/tekst per stop (mangler)
2. **Ikoner** — AI-genererede, erstatter tekst (mangler)
3. **GPS tracker** — fundament for navigation (mangler)

PC'en (Lenovo X1 Carbon Gen 13) ankom 4. marts. Yggdra (PC-versionen) adskilt fra Ydrasil (VPS). Videre udvikling venter på PC-setup.

**Kausal kæde 4: Organisering — fra kaos til struktur**
ChatGPT+Grok+Claude spredt (dec) → Ydrasil mono-repo (jan) → Trello (15/2) → Google Tasks (21/2) → Trello droppet (4/3) → projects/transport/ (mar).
Hvert organiseringsforsøg afspejlede voksende kompleksitet. Værktøjerne skiftede, men behovet var konstant: overblik over et projekt der voksede hurtigere end forventet.

---

## Opsummering

| Fase | Periode | Kerneaktivitet | Vigtigste beslutning |
|------|---------|----------------|---------------------|
| 1. Vision | Dec 2025 | Reverse-engineering, platform-valg | n8n som platform (6/12) |
| 2. Raffinering | Jan 2026 | n8n debugging, sorteringslogik | Claude Code > n8n (18/1) |
| 3. Gennembrud | Feb 2026 | Webapp-klon, kompendium v1-v5 | Professionelt format (18/2) |
| 4. Konsolidering | Mar 2026 | Projekt-organisering, sterilisering | PC-migration (4/3) |

**4 kausale kæder:**
1. Platform-evolution: Axiom → n8n → webapp-klon
2. Dokumentation: API-afkodning → bug-docs → kompendium → kildeindex
3. Sortering: manuelt → n8n → drag+drop webapp
4. Organisering: kaos → mono-repo → Trello → Google Tasks → projects/
