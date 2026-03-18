# Claude Code Token Optimization & Context Management

*Genereret 2026-01-31*

---

## 1. Context Window Management & Compaction

### Auto-Compaction
- Trigger: ~75% context usage (automatisk)
- `/compact` for manuel komprimering med custom instruktioner
- `/compact Focus on code samples and API usage`
- `/clear` når du skifter til urelateret arbejde

### Compact Instructions i CLAUDE.md
```markdown
# Compact instructions
When compacting, preserve: current task state, route data context,
file paths being worked on, and any pending actions.
```

### Cost Impact
Uden komprimering ved 75%: ~$9.00 for 20 beskeder. Med komprimering: ~$4.20 (**53% besparelse**).

---

## 2. Token Optimization Teknikker

### CLAUDE.md Best Practices
- Hold under **500 linjer** (officiel anbefaling)
- Kun essentials: tech stack, struktur, konventioner, pointers til skills
- Specialiserede instruktioner → **Skills** (on-demand)

### Progressive Disclosure (Vigtigst!)
1. **CLAUDE.md** (altid loaded, ~100-200 linjer): Overblik + pointers
2. **Skills** (on-demand, <500 linjer): Detaljerede instruktioner per domæne
3. **Kildefiler** (kun ved behov)

Token impact:
- ~100 tokens per skill metadata
- <5k tokens når skill aktiveres
- **98% reduktion** når skills er til stede men ikke brugt

### MCP Server Overhead
- Hver MCP server tilføjer tool definitions permanent
- `/context` for at se hvad der fylder
- Foretruk CLI tools: `gh`, `aws` osv. (mere kontekst-effektivt)
- `ENABLE_TOOL_SEARCH=auto:5` (trigger ved 5% context)

### Subagents (Task Tool)
- Isolér verbose operationer (tests, logs, docs)
- Output forbliver i subagentens kontekst, kun summary returneres
- Brug `model: haiku` for simple opgaver

### Extended Thinking
- Default: 31,999 tokens (billed som output)
- Reducer med: `MAX_THINKING_TOKENS=8000`
- Eller deaktiver i `/config`

---

## 3. Session Management

### Kommandoer
- `claude --continue` / `-c`: Fortsæt seneste session
- `claude --resume` / `-r`: Vælg specifik session
- `/rename` før `/clear` → nemt at finde og genoptage

### Multi-Session Pattern
1. Separate sessions for separate concerns
2. `/clear` ved domæneskift
3. Living plan i markdown fil (persisterer)
4. CLAUDE.md for tilstand der overlever alle sessions

---

## 4. Hooks & Automation

| Event | Hvornår | Kan blokere? |
|-------|---------|-------------|
| `SessionStart` | Session begynder | Nej |
| `PreToolUse` | Før tool udførelse | Ja |
| `PostToolUse` | Efter tool udførelse | Nej |
| `Stop` | Agent færdig | Kan tvinge videre |

### Preprocessing med Hooks
I stedet for at Claude læser 10.000-linjers log → hook grep'er for `ERROR` → kun relevante linjer.

---

## 5. Cost Reduction

### Prompt Caching
- **92% prompt reuse rate** naturligt
- Cache read: 90% billigere end base input
- Efter første request: cached content koster **10% af original pris**

### Model Priser (per million tokens)
| Model | Input | Output |
|-------|-------|--------|
| Opus 4.5 | $5.00 | $25.00 |
| Sonnet 4.5 | $3.00 | $15.00 |
| Haiku 4.5 | $1.00 | $5.00 |

- Gennemsnit: **$6/developer/dag**, under $12 for 90%
- Månedlig: **$100-200/developer** med Sonnet

### Power User Tips
1. Specifke prompts > vage (undgå bred scanning)
2. Plan mode (Shift+Tab) før implementation
3. Escape tidligt når Claude går forkert retning
4. `/rewind` for at gendanne checkpoints
5. Test inkrementelt: én fil, test, fortsæt

---

## Ydrasil-Specifikke Anbefalinger

1. **CLAUDE.md er velstruktureret** med 6 skills (progressive disclosure)
2. **Tilføj compact instructions** (se ovenfor)
3. **Monitor MCP overhead** med `/context`
4. **Brug Haiku for subagents** (simple opgaver)
5. **Hooks for Qdrant kontekst**: `get_context.py` som SessionStart hook

---

*Baseret på research fra Claude Code docs, community best practices, og 30+ kilder.*
