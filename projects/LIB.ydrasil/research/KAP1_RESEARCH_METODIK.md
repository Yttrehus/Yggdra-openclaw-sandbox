# Kapitel 1: Research-Metodik med AI

**Hvordan du systematisk researcher et emne og destillerer det til brugbar viden**

---

## 1.1 Hvorfor dette kapitel kommer først

Du kan ikke bygge en god videnbase med dårlig metode. Og de fleste AI-brugere researcher forkert: de stiller ét spørgsmål, får ét svar, og tror de har "researched" det. Det svarer til at læse bagsiden af én bog og tro du forstår emnet.

Rigtig research med AI handler om:
- **Bredde først, dybde efter** — survey landskabet før du graver
- **Flere perspektiver** — aldrig stol på én kilde eller én model
- **Verificering** — AI hallucinerer. Altid krydstjek.
- **Destillering** — Rå research er ubrugelig. Viden er destilleret research.

---

## 1.2 De 5 Research-Lag

Struktureret research følger en progression fra bredt til dybt:

### Lag 1: Bred Survey — "Hvad findes der?"
**Formål:** Kortlæg landskabet. Hvem er aktørerne? Hvad er begreberne? Hvor er debatten?

**Metode:**
- 3-5 parallelle web-søgninger med forskellige vinkler
- Læs officiel dokumentation + uafhængige reviews
- Notér navne, frameworks, og nøglebegreber

**Output:** En liste over emner, aktører, og åbne spørgsmål.

**Fælde:** At stoppe her. Lag 1 giver overblik men ingen dybde. Det er her vores eksisterende `/research/` surveys er — og det er ikke nok.

---

### Lag 2: Kilder & Eksperter — "Hvem ved noget?"
**Formål:** Find de primære kilder. Ikke blog posts OM emnet, men folk der HAR BYGGET det.

**Metode:**
- Identificér 3-5 nøgleeksperter/praktikere per emne
- Find deres primærkilder: talks, papers, docs, GitHub repos
- Kategorisér: akademisk vs. praktisk, vendor vs. uafhængig

**Output:** En kurateret kildeliste med vurdering af troværdighed.

**Princip: Kildetriangulering** — Hvis 3 uafhængige eksperter siger det samme, er det sandsynligvis sandt. Hvis kun én siger det, er det en mening.

---

### Lag 3: Dyb Research — "Hvad er sandheden?"
**Formål:** Gå i dybden. Læs primærkilderne. Forstå nuancerne.

**Metode: Triple Perspective**

For hvert emne, kør 3 parallelle research-agenter:

1. **Neutral Agent** — "Forklar dette emne objektivt. Hvad er fakta?"
2. **Blue Team (Advokat)** — "Argumentér FOR dette. Hvad er styrkerne? Hvornår er det den bedste løsning?"
3. **Red Team (Kritiker)** — "Argumentér IMOD dette. Hvad er svaghederne? Hvornår fejler det?"

**Hvorfor:** Ingen enkelt perspektiv giver hele billedet. Blue Team fanger styrker du overser. Red Team fanger fælder du ikke tænker på. Neutral sikrer fakta-grundlaget.

**Output:** En balanceret analyse med styrker, svagheder, og use cases.

---

### Lag 4: Vurdering — "Hvad betyder det for MIG?"
**Formål:** Oversæt abstrakt viden til din konkrete situation.

**Metode:**
- Hvad er min current state? (Hvad har jeg nu?)
- Hvad er min desired state? (Hvad vil jeg opnå?)
- Hvilke tradeoffs er acceptable? (Pris, kompleksitet, vendor lock-in)
- Er det en two-way door? (Kan jeg fortryde?)

**Output:** En beslutningsmatrix med konkrete anbefalinger.

---

### Lag 5: Destillering — "Hvad er den brugbare essens?"
**Formål:** Kog alt ned til viden du faktisk kan bruge.

**Metode:**
- Skriv som om du forklarer det til dig selv om 6 måneder
- Fjern alt der er "nice to know" men ikke "need to know"
- Bevar konkrete eksempler og handlingsanvisninger
- Embed i Qdrant så det er søgbart

**Output:** Et kapitel i din håndbog. Klart, konkret, handlingsorienteret.

---

## 1.3 Multi-Agent Research Patterns

### Mønster 1: Parallel Survey (Lag 1-2)

```
Orchestrator (du/Claude)
├── Agent A: Web-søgning vinkel 1
├── Agent B: Web-søgning vinkel 2
├── Agent C: Web-søgning vinkel 3
└── Agent D: Dokumentation/officielle kilder
    ↓
Syntese: Kombinér resultater, fjern dubletter, identificér huller
```

**Hvornår:** Når du starter et nyt emne og vil have bredt overblik hurtigt.

**Praktisk i Claude Code:**
```
Kør 3-5 Task agents parallelt med forskellige søgevinkler.
Hver agent returnerer struktureret output (ikke prosa).
Hovedagent syntetiserer til én rapport.
```

### Mønster 2: Triple Perspective (Lag 3)

```
Orchestrator
├── Neutral Agent: "Forklar X objektivt"
├── Blue Team Agent: "Argumentér FOR X"
└── Red Team Agent: "Argumentér IMOD X"
    ↓
Syntese: Balanceret analyse med styrker, svagheder, use cases
```

**Hvornår:** Når du skal forstå et emne i dybden og undgå bias.

### Mønster 3: Source Verification (Lag 2-3)

```
Research Agent finder påstand P
├── Verification Agent 1: Tjek P i kilde A
├── Verification Agent 2: Tjek P i kilde B
└── Verification Agent 3: Tjek P i officiel docs
    ↓
Confidence score: Bekræftet af 3/3, 2/3, eller 1/3 kilder
```

**Hvornår:** Når noget lyder for godt (eller for dårligt) til at være sandt.

### Mønster 4: Orchestrator-Workers (Lag 3-5)

```
Lead Agent (Opus) analyserer query
├── Worker 1 (Sonnet): Research delområde A
├── Worker 2 (Sonnet): Research delområde B
├── Worker 3 (Sonnet): Research delområde C
└── Citation Agent: Verificér alle påstande
    ↓
Lead Agent syntetiserer → færdig rapport
```

**Hvornår:** Komplekse emner der kræver mange delundersøgelser. Anthropics eget research-system bruger dette mønster — det slår single-agent med 90%.

**Nøgleindsigt fra Anthropic:** 80% af performance-variansen forklares af token-forbrug. Mere kontekst → bedre resultater. Det er ikke modellen der er flaskehalsen — det er konteksten.

---

## 1.4 Verificerings-Principper

### AI hallucinerer. Altid.

Det er ikke et spørgsmål om modellen er god nok. Selv de bedste modeller opfinder fakta. Derfor:

**Regel 1: Triangulering**
En påstand er kun verificeret når 3 uafhængige kilder bekræfter den. Én kilde = anekdote. To kilder = indikation. Tre kilder = evidens.

**Regel 2: Primærkilder over sekundære**
Officiel dokumentation > blog post > AI-genereret svar. Gå altid til kilden.

**Regel 3: Tjek datoer**
AI-viden har cutoff-datoer. Teknologi ændrer sig. Noget der var sandt i 2024 er måske forældet i 2026.

**Regel 4: Red Team dit eget output**
Når du har en konklusion, spørg eksplicit: "Hvad er galt med denne analyse? Hvad mangler? Hvor er mine blinde vinkler?"

**Regel 5: Confidence scoring**
For hver nøglepåstand, vurdér:
- **Høj (3/3 kilder):** Fakta, kan handles på
- **Medium (2/3 kilder):** Sandsynligt, verificér ved brug
- **Lav (1/3 eller AI-genereret):** Hypotese, kræver yderligere research

---

## 1.5 Token-Økonomi

Research koster tokens. Vær bevidst:

| Mønster | Token-forbrug | Estimeret kost |
|---------|---------------|----------------|
| Enkelt spørgsmål | ~2K tokens | ~$0.01 |
| Parallel survey (4 agenter) | ~40K tokens | ~$0.30 |
| Triple perspective | ~30K tokens | ~$0.20 |
| Fuld deep research (Lag 1-5) | ~200K tokens | ~$1-3 |
| Bog-destillering (som Nate/Miessler) | ~500K+ tokens | ~$5-15 |

**Tommelfingerregel:** Dyb research på ét emne koster $1-3. En komplet håndbog koster $10-30. Det er ingenting sammenlignet med værdien af at forstå noget rigtigt.

---

## 1.6 Vores Research-Workflow (praktisk)

Her er den konkrete workflow vi bruger i Ydrasil:

### Trin 1: Definér spørgsmålet
Skriv præcist hvad du vil vide. Ikke "fortæl mig om LLM'er" men "Hvilken LLM er bedst til kodegenerering i februar 2026, og hvorfor?"

### Trin 2: Parallel Survey
Kør 3-5 søgninger med forskellige vinkler. Gem resultater.

### Trin 3: Identificér kilder
Hvem er eksperterne? Hvad er de primære kilder? Lav en kildeliste.

### Trin 4: Triple Perspective
For de vigtigste emner: neutral + blue + red team.

### Trin 5: Verificér
Krydstjek nøglepåstande mod primærkilder.

### Trin 6: Destillér
Skriv det ned i klart, handlingsorienteret sprog. Embed i Qdrant.

### Trin 7: Review
Læs dit output næste dag. Mangler der noget? Er noget forkert?

---

## 1.7 Anti-Patterns — Hvad du IKKE skal gøre

1. **One-shot research** — Stil ét spørgsmål og acceptér svaret. Du får overfladisk viden med potentielle fejl.

2. **Echo chamber** — Brug kun én model/kilde. Du får dens bias.

3. **Volume over dybde** — 50 overfladiske søgninger slår ikke 5 dybe. Kvalitet > kvantitet.

4. **Ingen verificering** — "Claude sagde det, så det er sandt." Nej.

5. **Research uden destillering** — 100 sider rå noter er ubrugelige. Destillér altid.

6. **Perfectionism** — Vente på "komplet" research. Research er iterativ. Start, publicér, revidér.

---

## 1.8 Kilder

Denne metodik er baseret på:

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — De 5 composable patterns
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — Orchestrator-worker arkitektur, 90% improvement
- [Three Ways to Build Deep Research with Claude](https://paddo.dev/blog/three-ways-deep-research-claude/) — DIY, MCP, og Production patterns
- [Claude Code Subagents for Parallel Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/) — Praktiske parallel-patterns
- [Simon Willison: Parallel Coding Agents](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/) — Real-world erfaringer
- [Google: Getting AI Agents to Work Better](https://fortune.com/2025/12/16/google-researchers-ai-agents-multi-agent-getting-them-to-work/) — Threshold research (45% single-agent accuracy)
- Nate Jones: Context > Capability, Rumelt Strategy framework
- Daniel Miessler: Current → Desired State, Scaffolding > Models

---

*Sidst opdateret: 2026-02-09*
