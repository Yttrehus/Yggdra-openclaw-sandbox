# Nate Jones: Memory er AI's storste uloste problem

**Kilde:** https://youtu.be/JdJE6_OU3YA
**Hentet:** 2026-02-16
**Type:** YouTube video-analyse (fuld transskription)

---

## Overordnet tese

Nate Jones argumenterer for at **hukommelse er det storste uloste problem i AI** -- og det er et af de eneste problemer der bliver **vaerre, ikke bedre**. Efterhanden som intelligens-kapabiliteter vokser, halter hukommelsen bagefter. Han kalder det "the memory wall" -- et begreb fra chip-industrien der nu ogsaa gaelder paa systemdesign-niveau.

Hans kernebudskab: **Du kan ikke vente paa at vendors loeser det. Du skal bygge din egen hukommelsesarkitektur.**

---

## Del 1: Seks rodaarsager til hukommelsesproblemer

### 1. Relevansproblemmet (The Relevance Problem)
- Hvad der er relevant aendrer sig baseret paa: **opgavetype** (planlaegning vs eksekvering), **fase** (udforskning vs raffinering), **scope** (personligt vs projekt), og **state delta** (hvad er aendret siden sidst)
- **Semantisk lighed er kun en proxy for relevans** -- ikke en reel loesning
- RAG finder lignende dokumenter, men fejler naar du har brug for: "det dokument hvor vi besluttede X", "ignorer alt om klient A", "kun info efter 12. oktober"
- **"Der er ingen generel algoritme for relevans"** -- du har brug for menneskelig doemmekraft om opgavekontekst

### 2. Persistence-Precision tradeoff
- Gem alt → retrieval bliver stoejende og dyrt
- Gem selektivt → du mister info du faar brug for
- Lad systemet bestemme → det optimerer for det forkerte (recency, frequency, statistisk saliency vs reel vigtighed)
- **Menneskehukommelse loeser dette gennem "forgetting technology"**: lossy compression med emotionel og vigtigheds-vaegning

> **Vigtig indsigt om menneskelig hukommelse:**
> Nate beskriver menneskets hukommelse som et database-key system. Du skal huske "noeglen" for at hente erindringen. Korttidshukommelsen er ekstremt lossy -- du taber nogler medmindre du aktivt forsooger at fastholde dem. Derfor kan barndomsminder vaere tilgaengelige (staerke emotionelle nogler), mens du ikke kan huske hvad du lavede i torsdags.
>
> "Forgetting is a useful technology for us. AI systems don't have any of that. They either accumulate or they purge, but they do not decay."

### 3. Single Context Window antagelsen
- Storre context window ≠ bedre hukommelse
- **"A million token context window full of unsorted context is worse than a tightly curated 10,000"**
- Modellen skal stadig finde det relevante, parse relevans, ignorere stoej
- Du har ikke loest problemet -- du har gjort det dyrere
- **Den reelle loesning kraever multiple context streams med forskellige livscyklusser og retrieval-moenstre**

### 4. Portabilitetsproblemet
- Hver vendor bygger proprietaere hukommelseslag (ChatGPT memory, Claude recall, Cursor memory banks)
- Hukommelse bruges som moat/lock-in
- **For virksomheder er det en liability at vaere single-model** -- du SKAL vaere multimodel
- Loesning: Byg et portabelt kontekstbibliotek der overlever vendor-skift

### 5. Den passive akkumuleringsfejlslutning (Passive Accumulation Fallacy)
- De fleste memory-features antager at systemet selv finder ud af hvad det skal huske
- Dette fejler fordi systemet IKKE kan skelne mellem:
  - Praeferencer vs fakta
  - Projektspecifikt vs evergreen kontekst
  - Forealdet vs aktuel information
- **Systemet optimerer for kontinuitet, IKKE korrekthed** ("keep the conversation going")
- **"Useful memory fundamentally requires active curation"** -- du skal beslutte hvad der beholdes, opdateres og kasseres

### 6. Hukommelse er faktisk MULTIPLE problemer
Naar folk siger "AI memory" mener de ofte vidt forskellige ting:

| Type | Beskrivelse | Eksempel |
|------|-------------|---------|
| **Preferences** | Hvordan jeg foretraekker ting | Permanent key-value |
| **Facts** | Hvad er sandt om entiteter | Struktureret, kraever opdatering |
| **Knowledge** | Domaenekspertise | Parametrisk (vaegtet) eller ekstern |
| **Episodic** | Hvad vi har diskuteret | Konversationel, temporal, ephemeral |
| **Procedural** | Hvordan vi loeste det foer | Exemplarer, succeser og fejl |

> "Treating this problem as one problem guarantees you are going to solve none of the real problems well."

---

## Del 2: Otte principper for hukommelsesloesninger

### Princip 1: Memory er en arkitektur, ikke en feature
- Du kan ikke vente paa vendors
- Hvert vaerktoj vil have memory-kapabiliteter, men de loeser forskellige skiver
- **Du skal arkitektere hukommelse som en selvstaendig enhed der virker paa tvaers af alle dine vaerktoejer**

### Princip 2: Sepererer efter livscyklus, ikke bekvemmelighed
Tre klare lag:
- **Permanent**: Personlige praeferencer
- **Midlertidigt**: Projektfakta
- **Ephemeral**: Sessionstilstand / samtalekontekst

> "Mixing different life cycle states -- mixing permanent with temporary with ephemeral -- it just breaks memory."

### Princip 3: Match storage til query-moenster
Fire forskellige datatyper kraever fire forskellige storage-moenstre:

| Spoergsmaal | Datatype | Storage |
|-------------|----------|---------|
| Hvad er min stil? | Key-value | Simpel nogle-vaerdi |
| Hvad er klient-ID? | Struktureret/relationelt | Database |
| Hvad lignende arbejde har vi lavet? | Semantisk | Vektor/RAG |
| Hvad gjorde vi sidst? | Tidsserie | Event logs |

> "When people say 'We have our data lake and it's going to be a RAG' -- I'm like, why? Have you heard the word RAG repeated a hundred times like a magic spell for memory? It does not work that way."

### Princip 4: Mode-aware kontekst slaar volumen
- Planlaegning kraever **bredde** (alternativer, sammenligning)
- Eksekvering kraever **praecision** (constraints, fakta)
- **Retrieval-strategi skal matche opgavetypen**
- For chat-brugere: dette er hvad prompting faktisk goer -- giver mode-aware kontekst
- For agentic systemer: du skal arkitektere mode-awareness ind i systemet

### Princip 5: Byg portabelt som foersteklasses objekt
- Dit hukommelseslag skal overleve: vendor-skift, vaerktojsskift, model-skift
- **Obsidian og Notion naevnes som eksempler** paa platformuafhaengige loesninger
- Faellestraek for dem der lykkes: "They are obsessed with making sure the memory is configured correctly for them"

### Princip 6: Komprimering er kuratering
- Upload IKKE 40 siders dokument og haab paa det bedste
- **Goer komprimeringsarbejdet selv**: skriv briefen, identificer noeglefakta, angiv constraints
- "This is where judgment lives"
- Du kan bruge AI til at amplificere din doemmekraft (f.eks. struktureret ekstraktion), men **doemmekraften i komprimering er menneskelig**

### Princip 7: Retrieval kraever verifikation
- Semantisk soegning finder temaer godt, men fejler paa specifikke fakta
- **To-trins retrieval**: (1) Recall candidates, (2) Verificer mod ground truth
- Eksempel: Konsulentfirma idoemt $500.000 i bode fordi hallucinerede retsafgoerelser ikke blev verificeret
- For chat: mennesket verificerer
- For agentic systemer: automatisk verifikation via eval-agent

### Princip 8: Hukommelse compound'er gennem struktur
- Tilfaeldig akkumulering compound'er IKKE -- det skaber stoej
- **Struktureret hukommelse** med separation:
  - Evergreen kontekst -> et sted
  - Versionerede prompts -> et andet sted
  - Taggede exemplarer -> et tredje sted
- "Forgetting is a technology for us. In the same way, structured memory is a technology for LLM systems."

---

## Noglecitateter

> "AI systems are stateless by design, but useful intelligence requires state."

> "Semantic similarity is just a proxy for relevance. It is not a true solution."

> "Forgetting is a useful technology for us. AI systems don't have any of that. They either accumulate or they purge, but they do not decay."

> "A million token context window full of unsorted context is worse than a tightly curated 10,000."

> "Useful memory fundamentally requires active curation. You have to decide what to keep, what to update, and what to discard. And that is work."

> "The judgment in compression is human judgment. It may be human judgment that you amplify with AI, but it remains human judgment."

> "Treating this problem as one problem guarantees you are going to solve none of the real problems well."

> "Vendors fundamentally are treating this as a solve for infrastructure and not a solve for architecture."

---

## Praktisk anvendelse for Ydrasil

### Hvad vi allerede goer rigtigt
1. **Portabel arkitektur**: Qdrant som selvstaendig vektor-database, ikke bundet til een vendor
2. **Aktiv kuratering**: CLAUDE.md, skills, brain/ -- manuelt kureret kontekst
3. **Separation af livscyklusser**: Permanent (CLAUDE.md, skills) vs. midlertidigt (projekt-noter) vs. ephemeral (session logs)
4. **Komprimering**: Dagbog-systemet komprimerer sessions til noegleindsigter

### Hvad vi kan forbedre
1. **Multiple storage-moenstre**: Vi bruger primaert Qdrant (semantisk soegning). Vi mangler:
   - Key-value store til praeferencer og fakta (kan vaere simpelt JSON)
   - Struktureret/relationelt for rute-data og klient-info
   - Event logs med tidsstempler for "hvad gjorde vi sidst"
2. **Mode-awareness**: Systemet skelner ikke mellem planlaegnings- og eksekveringskontekst. Retrieval-strategi burde aendre sig efter opgavetype.
3. **Verifikation af retrieval**: Vi har ingen systematisk ground-truth-check paa hvad Qdrant returnerer. To-trins retrieval (recall + verify) ville oege praecision.
4. **Forgetting/decay**: Vi akkumulerer alt i Qdrant uden decay. Aeldredata burde nedprioriteres eller arkiveres -- ikke bare vaere der for evigt med samme vaegt.
5. **State delta tracking**: Vi tracker ikke eksplicit hvad der er aendret mellem sessions. En "changelog" per session/uge ville hjaelpe med at undgaa stale kontekst.
6. **Hukommelsestyper bor separeres**: I Qdrant boer vi have tydeligere collections/metadata for:
   - Preferences (permanent)
   - Project facts (temporary, versioneret)
   - Episodic (samtale-historik)
   - Procedural (loesningsmoenstre, exemplarer)

### Konkrete naeste skridt
1. Implementer metadata-tagging i Qdrant: `memory_type`, `lifecycle` (permanent/temporary/ephemeral), `created_at`, `stale_after`
2. Byg en simpel key-value store (JSON-fil) til permanente praeferencer og fakta
3. Tilfoej retrieval-verifikation: naar ctx returnerer resultater, lav en sekundaer check mod strukturerede fakta
4. Eksperimenter med decay/nedprioritering baseret paa alder og access-frequency

---

## Sammenfatning

Nate Jones' video er en af de mest strukturerede analyser af AI-hukommelsesproblemet. Hans seks rodaarsager forklarer HVORFOR det er svaert, og hans otte principper giver et konkret designframework.

**Kerneindsigten for Ydrasil**: Vi er paa rette vej med portabel arkitektur og aktiv kuratering, men vi behandler stadig hukommelse som ET problem (Qdrant) i stedet for MULTIPLE problemer med forskellige storage-, retrieval- og livscyklusmoenstre. Det naeste store fremskridt er at separere hukommelsestyperne og matche storage til query-moenster.

**Forbindelse til Nates bredere framework**: Dette bekraefter "Scaffolding > Models" -- vaerdien er ikke i modellen, men i den kontekstarkitektur du bygger omkring den. Hukommelse er det ultimative scaffolding-problem.
