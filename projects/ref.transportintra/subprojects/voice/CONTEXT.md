# Voice — Subproject

## Status: FRAGMENTERET (3 uafhængige dele, kun stop-beskrivelser er åbent)

## Hvad
Voice er IKKE ét projekt men 3 separate kontekster:

### 1. TTS i webapp — DONE
- `app/js/app.js:457-486` — `app.speak()` med `window.speechSynthesis` (dansk voice)
- Knap i UI der oplæser stop-info
- `Lists.js:206,287` — `txt2speak` attributter, `time2speech()` kald

### 2. Voice memo pipeline — DONE
**voice_pipeline.py:** Audio → Whisper → classify_intent → routing
- COMMAND/HIGH → huskeliste.md, OBSERVATION → Qdrant embedding
- Inbox: `/root/Yggdra/data/inbox`

**voice_memo_pipeline.py:** Google Drive watcher
- Overvåger `gdrive:Ydrasil/Data ind/ud/Indbakke - til AI/Voice memo/`
- Groq Whisper for transskription, Telegram-notifikation

### 3. Stop-beskrivelser via voice — PLANLAGT (det eneste åbne)
- Chauffør indtaler noter om leveringsdetaljer, adgangsforhold, kontaktpersoner
- Gemmes som metadata på rutedata, søgbar via app
- **Kun 1 datapunkt:** transport/NOW.md nævner det som prioritet
- Ingen kode, ingen design, ingen implementeringsplan

### 4. Voice Android-app — BYGGET
- `voice-app/` — Android WebView-wrapper for `voice.html`
- `MainActivity.java` loader `https://app.srv1181537.hstgr.cloud/voice.html`
- APK: `app/ydrasil-voice.apk` (2.9 MB)

## Session-referencer
- **2026-02-19:** ~20 min voice memo med feedback på kompendium v2 (pipeline i brug)
- **transport/NOW.md:** "Stop-beskrivelser — voice/tekst per stop" som næste prioritet

## Vurdering
TTS og voice pipelines er færdige. Android-app er bygget.
Et voice-subproject giver kun mening for stop-beskrivelser (3).
Stop-beskrivelser har kun 1 datapunkt — markeret THIN for den del.
