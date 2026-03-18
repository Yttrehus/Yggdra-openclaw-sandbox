# Voice Integration

**Dato:** 2026-03-12 (opdateret 2026-03-15)
**Klar til:** Backlog (scope uafklaret)

## Opsummering
- Voice-integration i Yggdra-systemet
- Tre mulige retninger — bør vælge én:
  1. **Voice-to-text** (mest oplagt): Diktere noter, beskeder, idéer → tekst. Yttre bruger allerede voice memos.
  2. **Voice commands:** Styr Claude Code med stemme. Kræver pipeline (mic → transcription → CLI).
  3. **TTS:** Claude læser output op. Nice-to-have, ikke kernebehov.
- ElevenLabs allerede installeret (~40 kr/mnd)

## Origin Story
Parkeret i PLAN.md idé-parkering. Yttre bruger allerede voice memos som input-metode.

## Eksisterende research (lokalt i projects/research/ydrasil/)
- `research/voice_app_project_state.md` — tidligere voice app projekt-state
- `research/whisper_pricing_2026.md` — Whisper pricing research
- `docs/VOICE_ASSISTANT_RESEARCH.md` — voice assistant research
- `docs/VOICE_DIARY_20260213_ANALYSE.md` — voice diary analyse

## Rå input
**Fra PLAN.md idé-parkering:**
> Voice-integration

tilføjelse fra Yttre: det handler ligeså meget hvis ikke mere at designe sin egen stemme, kadence m.m. grok gør der at mens brugerens tale bliver transkriberet læser grok løbende , det er mere virkeligheds nært og den svarer jo nærmest så snart man er færdig med at tale. mennesker tænker jo også mens den anden snakker. den kunne jo være en del af et større projekt. et dashboard hvor jeg kan læse downloade uploade filer, voice chat,. idealet ser vi en scene fra her hvor hun tegner hvordan  det ville se ud hvis folk sked ud af albuen. naturligt flow fra tale til generede billede har stærk effekt hos mennesker