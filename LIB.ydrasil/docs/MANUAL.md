# Ydrasil Manual

Levende dokument. Yggdra vedligeholder, Kris godkender.

---

## Agenterne

Du taler med Claude som altid. Under motorhjelmen arbejder specialister.

| Agent | Hvad den gør | Hvornår |
|-------|-------------|---------|
| **Yggdra** | Ser alt. Finder blinde vinkler. Orkestrerer. | "hvad har vi overset?", session-start, morgen-review |
| **Byggeren** | Koder i isolation. Smadrer aldrig produktion. | "byg X", "fix Y", "prototype Z" |
| **Forskeren** | Bedste viden, færrest tokens. | "hvad ved vi om X?", research, papers |
| **Revisoren** | Din CFO. Penge, skat, regler. | "hvor mange penge?", bogføring, udlæg |

De er alle Claude. Men de husker hver deres ting.

---

## Worktrees — den mentale model

**Skrivebord (main):** Det du ser. Instant deploy. Hverdagen.

**Værkstedsbord (worktree):** Et isoleret arbejdsbord. Byggeren arbejder her. Intet påvirker produktion.

Når Byggeren er færdig:
- `scripts/` ændringer → merges automatisk
- `app/` ændringer → du godkender først (fordi det er live)

---

## Mirror-princippet

Alle agenter gengiver hvad de forstår FØR de handler.

**Hvorfor:** LLM'er simulerer forståelse. Mirror tvinger dem til at VISE den, så misforståelser fanges tidligt.

**Eksempel:**
- Du: "fix sort-knappen så den husker valget"
- Agent: "Jeg forstår det som: sort-knappen skal gemme brugerens valg i localStorage og genoprette det ved næste besøg. Korrekt?"

---

## Kendte fælder

Friktionsmønstre vi har lært af. Vokser løbende.

1. **Overplanlægning** — Vi har brugt 4 runder på at planlægge i stedet for at bygge. Planlæg i max 1 runde, byg derefter.
2. **Falsk selvsikkerhed** — Claude TROR den forstår men gør det ikke. Mirror-princippet er modgiften.
3. **Rigtige idéer skudt ned** — Claude har afvist Kris' korrekte intuitioner. Reglen: når Kris insisterer, er det sandsynligvis Claude der mangler kontekst.
4. **Værktøjer glemt** — Nano Banana Pro, research.py, ctx — Claude "glemmer" værktøjer. Agent-definitions og skills loader dem.

---

## Rejsen

117 genstarter. Hver med lektier.

### Vendepunkter
- **2026-02-25:** Multi-agent arkitektur implementeret. 4 identiteter med egen hukommelse.
- (Opdateres løbende)

---

## Visualiseringer

Sort/hvid. Farver kun når de giver mening. Formål: fælles forståelse.

- Mindmap-app: `app/mindmap/`
- Systemanatomien: `docs/system_anatomy.html`
- (Opdateres når nye visualiseringer virker bedre)
