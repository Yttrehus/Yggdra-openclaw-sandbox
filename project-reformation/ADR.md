# ADR-001: Project Reformation

## 0. Metadata
- **Stage:** DLR
- **Status:** Active
- **Oprettet:** 2026-03-11
- **Sidst opdateret:** 2026-03-11
- **Ejer:** Yttre + Claude

## 1. Origin Story
Project Reformation opstod d. 11/3-2026 under session 9. Det startede ikke som ét projekt men som en kaskade af frustrationer: auto-chatlog var halvfærdig, checkpoint opdaterede NOW.md men glemte PLAN.md, implementation journals eksisterede men var tynde og kontekstløse, og nye idéer druknede i et system der ikke havde infrastruktur til at håndtere dem. Yttre gik fra forstanden over at kontekst forsvandt mellem sessioner — ikke fordi ideerne var dårlige, men fordi der ikke var et stillads der fangede dem. Samtalen eskalerede fra "kan chatloggen opdatere sig selv?" til "hele projektstyringen mangler en livscyklus." En parallel samtale med Google AI Mode validerede idéen om en 4-stage pipeline (PoC → DLR → SIP → BMS) med levende ADR-dokumenter. Det blev klart at Basic Setup ikke bare var "opsætning af et udviklermiljø" — det var ved at blive et framework for hvordan Yttre arbejder med AI.

## 2. Current State
DLR-fase. ADR-template er designet og skrevet til disk. Pipeline-navne besluttet (PoC/DLR/SIP/BMS) efter flere iterationer (TRL/DLR/SIP/BMS → RAW/DEV/STG/CORE → PoC/DLR/SIP/BMS). Selve Project Reformation lever isoleret i sin egen mappe — intet er rørt i det eksisterende filsystem endnu. Næste skridt er README'er/governance for de fire stages, derefter mapping af eksisterende filer til ny struktur. Denne sektion vil med tiden beskrive hvordan reformationen faktisk gik: hvad virkede, hvad måtte justeres, og hvad vi ikke forudså.

## 3. Problem Statement
- **Hvad:** Implementationer i Basic Setup har ingen formel livscyklus. De opstår i samtaler, halvimplementeres, og mister kontekst mellem sessioner. PLAN.md afspejler ikke virkeligheden. Implementation journals er tynde.
- **Hvorfor:** Det fører til tabt arbejde, gentagne diskussioner, og frustration. Yttre har gentagende gange mistet overblik over hvad der er gjort, hvad der er halvfærdigt, og hvad der bare er en idé.

## 4. Target State
Ethvert modul/projekt har en ADR der følger det fra fødsel til arkiv. Fire stadier (PoC → DLR → SIP → BMS) giver øjeblikkeligt overblik. Changelog i dagbogsstil bevarer fuld kontekst — om 5 år kan man samle en arkiveret ADR op og forstå alt uden at grave i chatloggen. Intet kræver hukommelse. Stilladset fanger det.

## 5. Architecture & Trade-offs
- **Beslutning:** 4-stage pipeline (PoC → DLR → SIP → BMS) med levende ADR-dokumenter. ADR bor med det den beskriver, ikke i en central mappe. ADR-INDEX.md i roden linker til alle. Fraktal: hvert projekt kan have sin egen pipeline-instans.
- **Konsekvenser:** Mere dokumentation per modul. Risiko for bureaukrati. Afbødes ved stram template + dagbogsstil changelog (nok kontekst, ikke en roman). Mappestrukturen kræver en omstrukturering af Basic Setup.

## 6. Evaluation
- Kan vi åbne en ADR om 6 måneder og forstå fuld kontekst uden chatloggen?
- Reducerer det "hvad lavede vi sidst?"-spørgsmål ved session-start?
- Føles det som sikkerhedsnet eller bureaukrati?
- Opdateres ADR'er faktisk løbende, eller glemmes de?

## 7. Exit Criteria
- **Promotion til SIP:** ADR-template testet på mindst 2 moduler. README'er for alle 4 stages skrevet. Eksisterende filer mappet til ny struktur.
- **Promotion til BMS:** Brugt friktionsfrit i 5+ sessioner. Checkpoint-skill scanner ADR'er automatisk.
- **Demotion:** Hvis ADR'er konsekvent ikke opdateres → systemet er for tungt → simplificér template.
- **Sunset:** Hvis vi efter 10 sessioner stadig glemmer at opdatere → forkert design → skrot og find anden tilgang.

## 8. Changelog
- 2026-03-11 (session 9, ~09:30): Det hele startede med et spørgsmål om automatisk chatlog-opdatering. Yttre observerede at Claude Codes .jsonl sessionsfiler vokser kontinuerligt men aldrig omdannes til læsbar chatlog automatisk. En parser-prototype (chatlog-engine.js) blev bygget i chatlog-test/ — den virkede, men designet var ikke færdigt da Claude gik i bygge-mode for tidligt. Yttre kalibrerede: "spørg før du bygger."

- 2026-03-11 (~10:00): Diskussionen eskalerede til implementation journals, ADR-format, og staging-mappe for prototyper. Yttre foreslog at ADR'er bor med det de beskriver (ikke central mappe). Plan+NOW+Progress sammensmeltning blev diskuteret og parkeret som idé. Tre iterationer af chatlog-design: navigationslinks, referater, retskrivning — alt parkeret som fremtidige forbedringer.

- 2026-03-11 (~11:00): Google AI Mode session validerede og forfinede idéen. Pipeline-navne gennemgik flere iterationer: TRL/DLR/SIP/BMS → RAW/DEV/STG/CORE → endelig landing på PoC/DLR/SIP/BMS. Fraktal struktur bekræftet: hvert projekt har sin egen pipeline-instans. ADR-template fusioneret fra Google-session + vores iterationer.

- 2026-03-11 (~13:00): PLAN.md afslørede et strukturelt problem: step 2-10 i M5 var gjort men ikke afkrydset. Checkpoint opdaterer NOW.md men rører ikke PLAN.md. Dette understregede behovet for Project Reformation. ADR-template færdigdesignet: Origin Story i toppen (kontekst først), Current State med narrativ, dagbogsstil changelog, Original ADR som frosset snapshot til sidst. Template og ADR skrevet til disk i project-reformation/.

## 9. Backlog
- README'er/governance-manualer for PoC, DLR, SIP, BMS (punkt 3 i planen)
- Map eksisterende filer til ny struktur (punkt 4)
- ADR-INDEX.md i roden
- Test ADR-template på auto-chatlog og checkpoint som første moduler
- Navigationslinks i chatlog-engine.js
- Plan-konsolidering (plan+now+progress → ét dok) — parkeret som eksperiment
- Lokal LLM (Ollama) til opsummering/nøgleord — parkeret som fremtidigt projekt
- Opdatér checkpoint-skill til at scanne ADR'er og PLAN.md checkboxes
- Overvej om project-reformation/ selv skal leve i en PoC/DLR/SIP/BMS-struktur (meta!)

## 10. Original ADR

### Problem Statement
- Hvad: Implementationer (auto-chatlog, checkpoint, skills, hooks) har ingen formel livscyklus. De opstår i samtaler, halvimplementeres, og mister kontekst mellem sessioner.
- Hvorfor: Det fører til tabt arbejde, gentagne diskussioner, og PLAN.md der ikke afspejler virkeligheden.

### Target State
Ethvert modul/projekt har en ADR der følger det fra idé til arkiv. Livscyklus-stadier (PoC → DLR → SIP → BMS) giver øjeblikkeligt overblik over modenhed. Intet kræver hukommelse — stilladset fanger alt.

### Architecture & Trade-offs
- Beslutning: 4-stage pipeline med levende ADR-dokumenter. ADR bor med det den beskriver. Fraktal: hvert projekt kan have sin egen instans af pipelinen.
- Konsekvenser: Mere dokumentation per modul. Risiko for bureaukrati. Afbødes ved at holde ADR-templaten stram og changelog i dagbogsstil.

### Evaluation
- Kan vi åbne en ADR om 6 måneder og forstå fuld kontekst uden chatloggen? (Ja = virker)
- Reducerer det antallet af "hvad lavede vi sidst?"-spørgsmål ved session-start? (Ja = virker)
- Føles det som bureaukrati eller som et sikkerhedsnet? (Bureaukrati = juster)

### Exit Criteria
- Promotion til SIP: ADR-template testet på mindst 2 eksisterende moduler (auto-chatlog + checkpoint). README'er for PoC/DLR/SIP/BMS skrevet.
- Promotion til BMS: Brugt friktionsfrit i 5+ sessioner. Checkpoint-skill opdateret til at scanne ADR'er.
- Demotion: Hvis ADR'er konsekvent ikke opdateres → for tungt → simplificér.
- Sunset: Hvis vi efter 10 sessioner stadig glemmer at opdatere ADR'er, er systemet forkert designet.
