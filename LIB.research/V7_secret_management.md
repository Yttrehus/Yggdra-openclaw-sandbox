# V7 Secret Management Protocol

## Formål
Sikre at reelle API-nøgler og credentials aldrig bliver committed til repository'et under V7 integrationen.

## Standard
1. **Lokation:** Alle hemmeligheder gemmes i `data/secrets/`.
2. **Format:** JSON filer (f.eks. `google_creds.json`, `notion_keys.json`).
3. **Ignorering:** `.gitignore` er sat op til at ignorere alle JSON filer i `data/secrets/` undtagen `secrets.example.json`.
4. **Indlæsning:** Brug `scripts/load_secrets.py` (skal bygges) til at hente credentials sikkert ind i agent-sessions.

## Afhængigheder
- OpenClaw environment variables (hvis tilgængelige).
- Krypteret opbevaring på VPS.

## Status
Roadmap V7.1 Readiness: **Høj**.
