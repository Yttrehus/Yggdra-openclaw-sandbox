# Skill: checkpoint

## Formål
Samler den daglige drift-loop i ét kald. Sikrer kontinuitet og arkivering.

## Instruktion
Når brugeren kører `/checkpoint`, skal du gøre følgende i rækkefølge:

1. **Auto-chatlog:** Kør `node projects/auto-chatlog/chatlog-engine.js` (hvis den findes) for at opdatere `chatlog.md`.
2. **State-opdatering:**
   - Opdatér `CONTEXT.md` med de seneste handlinger og beslutninger.
   - Opdatér `PROGRESS.md` med et narrativt afsnit om sessionen.
   - Afkryds færdiggjorte opgaver i `projects/0_backlog/TRIAGE.md` eller relevante briefs.
3. **Commit:**
   - Kør `git add .`
   - Kør `git commit -m "checkpoint: session <nummer> - <kort beskrivelse>"`
4. **Push:** Kør `git push origin main`.

## Feedback
Efter hver kørsel skal du skrive en kort status på hvad der blev opdateret, og om der var fejl.
