# Always-Listening Voice Assistant for Android: Technical Research Report

## 1. Wake Word / Keyword Detection (On-Device)

### 1.1 Porcupine by Picovoice (Recommended)

**What it is:** A commercial, on-device wake word engine using deep neural networks. Version 4.0.1 released December 2025.

**Key specs:**
- 97%+ detection accuracy with <1 false alarm per 10 hours
- CPU usage <4% on a Raspberry Pi 3 (even lighter on modern Android)
- Custom wake words trained in seconds by typing the phrase in the Picovoice Console
- Android SDK with `PorcupineManager` for integrated audio recording
- Runs in foreground service on Android (confirmed by developers)

**Danish support:** NOT officially supported. Supported languages are English, Chinese, French, German, Italian, Japanese, Korean, Portuguese, Spanish. Danish may be available for commercial customers on a case-by-case basis. However, since "ydrasil" uses phonemes found across supported languages, it may work acceptably with the English or German model. Testing needed.

**Pricing:** Free tier for up to 3 active users/month (personal/non-commercial). Paid plans start at $6,000/year. Free tier is sufficient for a single-user app.

**Battery:** Designed specifically for always-on use. Lightweight neural network avoids the battery drain of cloud-based ASR. No specific mAh figures published, but significantly better than streaming audio to cloud.

Sources: [Porcupine](https://picovoice.ai/platform/porcupine/), [Android Quick Start](https://picovoice.ai/docs/quick-start/porcupine-android/), [Pricing](https://picovoice.ai/pricing/), [Wake Word Guide 2025](https://picovoice.ai/blog/complete-guide-to-wake-word/)

### 1.2 OpenWakeWord

**What it is:** Open-source (Apache 2.0) wake word framework using Google's audio embedding model + small classifier. Popular in the Home Assistant community.

**Key specs:**
- Models are ~1-2 MB each
- Can run 15-20 models simultaneously on a single Raspberry Pi 3 core
- Trained with 100% synthetic TTS speech (no manual data collection needed)
- Android Kotlin library available: [`openwakeword-android-kt`](https://github.com/Re-MENTIA/openwakeword-android-kt) (Maven: `xyz.rementia:openwakeword:0.1.5`)

**Danish support:** Only English officially supported. The training pipeline depends on English multi-speaker TTS models. Training a Danish wake word would require supplying custom Danish TTS clips and manual effort. The underlying Google embedding model is language-agnostic (trained on 6000+ languages), so the feature extraction may work for Danish phonemes, but this is untested.

**Verdict:** Best open-source option but requires ML effort for Danish. The Android Kotlin library makes integration feasible.

Sources: [OpenWakeWord GitHub](https://github.com/dscripka/openWakeWord), [Android Kotlin lib](https://github.com/Re-MENTIA/openwakeword-android-kt), [Non-English discussion](https://github.com/dscripka/openWakeWord/discussions/52)

### 1.3 Mycroft Precise

**What it is:** RNN-based wake word listener, originally from Mycroft AI (closed 2023). Now maintained as forks under OpenVoiceOS.

**Key specs:**
- Trains on sound patterns, not word patterns (language-agnostic by design)
- Requires 50-100 wake word samples for training
- Linux-only; no native Android support
- Could potentially be converted to TFLite for Android deployment

**Verdict:** Deprecated upstream, Linux-focused. Not recommended for a new Android project.

Sources: [Mycroft Precise GitHub](https://github.com/MycroftAI/mycroft-precise), [OVOS plugin](https://github.com/OpenVoiceOS/ovos-ww-plugin-precise)

### 1.4 Android VoiceInteractionService

Built-in Android API for voice activation. Limited to "OK Google"-style triggers. Cannot define custom wake words. Not suitable for this use case.

### 1.5 Wake Word Comparison

| Engine | Custom Words | Danish | Android | Battery | License | Effort |
|--------|-------------|--------|---------|---------|---------|--------|
| **Porcupine** | Yes (seconds) | No (maybe commercial) | Native SDK | Excellent | Free tier / $6K | Low |
| **OpenWakeWord** | Yes (TTS training) | No (hackable) | Kotlin lib | Good | Apache 2.0 | Medium |
| **Mycroft Precise** | Yes (50+ samples) | Possible | No | Unknown | Apache 2.0 | High |

**Recommendation:** Start with **Porcupine** for rapid prototyping. The wake word "ydrasil" has enough syllables (3+) and distinct phonemes to work well. Test with the English model first. If Picovoice cannot support Danish commercially, fall back to OpenWakeWord with custom training.

---

## 2. Android Foreground Service for Audio

### 2.1 Android 14/15 Requirements

Starting with Android 14 (API 34), background audio recording requires strict compliance:

1. **Manifest declarations:**
   - `android:foregroundServiceType="microphone"` on the service
   - `<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />`
   - `<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />`
   - `<uses-permission android:name="android.permission.RECORD_AUDIO" />`

2. **Runtime constraints:**
   - Must request `RECORD_AUDIO` permission while the app is in the foreground
   - Must start the foreground service while the app has a visible activity
   - Cannot start microphone foreground service from `BOOT_COMPLETED` on Android 14+
   - Must show a persistent notification

3. **Android 15 additions:**
   - 6-hour timeout on `dataSync` and `mediaProcessing` service types
   - **Microphone type is NOT subject to the 6-hour timeout** -- it can run indefinitely
   - Only top app or audio-related foreground services can request Audio Focus

**Key implication:** The user must open the app at least once after boot to start the listening service. The service can then run indefinitely with a persistent notification.

Sources: [Android FGS Types](https://developer.android.com/about/versions/14/changes/fgs-types-required), [FGS Service Types](https://developer.android.com/develop/background-work/services/fgs/service-types), [Android 15 Changes](https://developer.android.com/about/versions/15/changes/foreground-service-types)

### 2.2 Native Kotlin vs Capacitor

| Factor | Native Kotlin | Capacitor/Ionic |
|--------|--------------|-----------------|
| Audio latency | Direct `AudioRecord` / Oboe API | WebView bridge overhead |
| Background services | Full control, `ForegroundService` | Requires custom plugin |
| Background performance | Baseline | Up to **9x slower** for background tasks |
| Wake word integration | Native SDK available | Needs bridging |
| Real-time audio processing | Optimal | Not designed for it |
| Development speed | Slower | Faster with web skills |
| Code sharing with web | None | Full |

**Verdict:** For an always-on audio app with wake word detection, VAD, and audio processing, **native Kotlin is strongly recommended.** The performance gap is too significant. Capacitor adds a WebView layer that creates unnecessary overhead and complexity for this use case.

**Hybrid approach:** Build the audio pipeline as a native Android service. If you need a web-based UI for settings/dashboard, embed a WebView or use Capacitor only for the UI layer while the audio service runs natively.

Sources: [Capacitor Audio Recorder](https://capawesome.io/plugins/audio-recorder/), [Capacitor Foreground Service](https://capawesome.io/plugins/android-foreground-service/), [Background Services in Capacitor](https://jscrambler.com/blog/background-services-in-ionic-capacitor)

---

## 3. Voice Activity Detection (VAD)

### 3.1 Silero VAD (Recommended)

**What it is:** Pre-trained deep learning VAD, MIT licensed, trained on 6000+ languages.

**Key specs:**
- Model size: 1.8 MB
- Processing time: <1ms per audio chunk (30+ ms) on a single CPU thread
- Supports 8 kHz and 16 kHz sample rates
- Language-agnostic (works for Danish)

**Android integration:** Dedicated [`android-vad`](https://github.com/gkonovalov/android-vad) library supports:
- Silero VAD DNN (ONNX Runtime Mobile)
- WebRTC VAD GMM
- Yamnet VAD DNN
- Configurable silence duration (default 300ms) and speech duration (default 50ms)

**Recommended configuration:**
```
Sample Rate: 16 kHz
Frame Size: 512
Mode: NORMAL
Silence Duration: 300ms
Speech Duration: 50ms
```

Sources: [Silero VAD GitHub](https://github.com/snakers4/silero-vad), [Android VAD Library](https://github.com/gkonovalov/android-vad), [VAD Comparison 2025](https://picovoice.ai/blog/best-voice-activity-detection-vad-2025/)

### 3.2 WebRTC VAD

Google's older GMM-based VAD. Faster but less accurate than Silero. Available in the same `android-vad` library. Good as a fallback for ultra-low-power scenarios.

### 3.3 Chunking Strategy

For continuous recording with VAD:

1. **Wake word detected** -> Start buffering audio
2. **Silero VAD monitors** -> Marks speech segments
3. **Silence threshold** (e.g., 2-3 seconds) -> Triggers end of utterance
4. **Speech segments** -> Concatenated and sent for transcription
5. **Non-speech segments** -> Discarded (saves storage and API cost)

For "journal" mode (continuous recording):
- Buffer audio in 30-second chunks
- Run VAD on each chunk
- Keep only chunks with speech (or >50% speech)
- Compress with Opus and queue for batch transcription

---

## 4. Speech-to-Text Options

### 4.1 Comparison Table

| Service | Danish Support | Pricing | Streaming | Diarization | Best For |
|---------|---------------|---------|-----------|-------------|----------|
| **Deepgram Nova-3** | Yes (da-DK) | $0.0065-0.0077/min | Yes | Yes | Best Danish + real-time |
| **OpenAI Whisper API** | Yes | $0.006/min | No | No | Cheapest batch |
| **GPT-4o Mini Transcribe** | Yes | $0.003/min | No | No | Cheapest overall |
| **Google Chirp 3** | Likely (85+ langs) | $0.016/min | Yes | Yes | Best features |
| **AssemblyAI Universal** | Yes (batch only) | $0.0025/min ($0.15/hr) | No Danish streaming | Yes (95 langs) | Cheapest per hour |
| **Local Whisper (on-device)** | Yes (large model) | Free | N/A | No | Offline/privacy |

### 4.2 Deepgram Nova-3 (Recommended for Danish)

- Explicitly expanded to Danish (da-DK) in 2025
- Handles Danish phonetics (which differ sharply from spelling)
- Real-time streaming available
- $200 free credits for new accounts (~750 hours)
- Low latency, handles background noise well

Sources: [Deepgram Danish Support](https://deepgram.com/learn/deepgram-expands-nova-3-with-german-dutch-swedish-and-danish-support), [Deepgram Pricing](https://deepgram.com/pricing)

### 4.3 OpenAI Whisper / GPT-4o Transcribe

- Danish supported but smaller models struggle significantly ("Jeg fucking elsker tebirkes" -> "Ja, fucking, ells godt, taet biogis" on whisper-tiny)
- Use medium/large models or GPT-4o Transcribe for acceptable Danish quality
- GPT-4o Mini Transcribe at $0.003/min is the cheapest API option
- No streaming -- batch only
- Tip: Run audio through ffmpeg at 2-3x speed before transcription to reduce cost with minimal quality loss

Sources: [OpenAI Pricing](https://platform.openai.com/docs/pricing), [Whisper Danish Fine-tuning](https://medium.com/@rasgaard/fine-tuning-whisper-tiny-for-danish-for-free-c77f4dac9d94)

### 4.4 Google Cloud Speech-to-Text Chirp 3

- 85+ languages, Danish likely included (verify via locations API)
- Built-in speaker diarization and automatic language detection
- Built-in denoiser
- $0.016/min standard, volume discounts to $0.004/min
- Available in europe-west2 and europe-west3 (good for Danish data residency)

Sources: [Chirp 3 Docs](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3), [GCP STT Pricing](https://brasstranscripts.com/blog/google-cloud-speech-to-text-pricing-2025-gcp-integration-costs)

### 4.5 Local Whisper on Android

- Feasible with ONNX Runtime Mobile or whisper.cpp
- INT8 quantized tiny/base models: ~40 MB, near real-time on flagship phones
- Pixel 7: ~2 seconds for 30-second audio clip (tiny model)
- Budget phones: 2-4x real-time (too slow for practical use)
- **Danish quality on tiny/base is poor.** Medium model needed, which is 1.5 GB and too slow for real-time on mobile.

**Verdict:** Local Whisper on Android is viable for English but NOT recommended for Danish due to the quality/size tradeoff. Use API-based transcription for Danish.

Sources: [ONNX Whisper Android Example](https://github.com/microsoft/onnxruntime-inference-examples/blob/main/mobile/examples/whisper/local/android/readme.md), [Edge ASR Guide](https://www.ionio.ai/blog/running-transcription-models-on-the-edge-a-practical-guide-for-devices)

### 4.6 Danish STT Recommendation

**Primary:** Deepgram Nova-3 -- purpose-built Danish support, streaming capable, good pricing with $200 free credits.

**Fallback:** GPT-4o Mini Transcribe at $0.003/min for batch transcription (half the cost of Whisper API).

**Budget estimate for daily use:**
- Assume 2 hours of actual speech per day after VAD filtering
- Deepgram: 120 min x $0.0077 = $0.92/day = ~$28/month
- GPT-4o Mini: 120 min x $0.003 = $0.36/day = ~$11/month

---

## 5. Similar Open Source Projects

### 5.1 Notely Voice (Android, F-Droid)
- Voice-to-text notes app on Android
- On-device transcription after model download
- Multiple language support
- Available on [F-Droid](https://f-droid.org/en/packages/com.module.notelycompose.android/)

### 5.2 Scriberr (Self-hosted)
- Self-hosted audio transcription with speaker diarization
- Chat with your transcripts via LLM
- Privacy-focused (no cloud)
- [GitHub](https://github.com/rishikanthc/Scriberr)

### 5.3 OVOS (Open Voice OS)
- Full voice assistant framework, successor to Mycroft
- Modular: wake word + STT + TTS + skills
- Pre-Wake-VAD feature (2025)
- HiveMind for distributed setup
- **No Android app** -- Linux/embedded focused
- Could serve as backend voice pipeline
- [Website](https://www.openvoiceos.org/)

### 5.4 Home Assistant Voice Pipeline
- Uses OpenWakeWord for wake word detection
- Integrates with Whisper for STT
- Wyoming protocol for component integration
- Designed for smart home, not mobile
- [HA Wake Words](https://www.home-assistant.io/voice_control/create_wake_word/)

### 5.5 Meetily / Hyprnote
- Open source meeting assistants with local processing
- Hyprnote: custom 1.1 GB summarization model that runs locally
- Desktop-focused, not Android
- [Meetily](https://meetily.zackriya.com/), [Hyprnote](https://hyprnote.com/blog/open-source-meeting-transcription-software/)

**Verdict:** No existing open-source project does exactly what is needed (always-on Android + wake word + Danish STT + AI processing). The closest architecture inspiration is OVOS (modular pipeline) combined with the Android VAD and wake word libraries.

---

## 6. Architecture Recommendation

### 6.1 Recommended Stack

```
+------------------------------------------+
|          ANDROID APP (Native Kotlin)      |
|                                           |
|  +-------------------------------------+ |
|  |   Foreground Service (microphone)    | |
|  |                                      | |
|  |  AudioRecord (16kHz, mono)           | |
|  |       |                              | |
|  |       v                              | |
|  |  Porcupine Wake Word Detection       | |
|  |  ("ydrasil journal", "ydrasil        | |
|  |   message", "ydrasil stop")          | |
|  |       |                              | |
|  |       v (wake word detected)         | |
|  |  Silero VAD (speech segmentation)    | |
|  |       |                              | |
|  |       v                              | |
|  |  Opus Encoder (24kbps)               | |
|  |       |                              | |
|  |       v                              | |
|  |  Local Buffer / Queue                | |
|  +------+------------------------------+ |
|          |                                |
|  +-------v-----------------------------+ |
|  |   Network Layer                      | |
|  |   POST audio chunks to backend       | |
|  +------+------------------------------+ |
+----------+--------------------------------+
           |
           v
+------------------------------------------+
|     BACKEND (FastAPI on VPS)              |
|                                           |
|  /api/voice/transcribe                    |
|    -> Deepgram Nova-3 (Danish STT)        |
|    -> Transcript returned                 |
|                                           |
|  /api/voice/process                       |
|    -> Claude API (AI processing)          |
|    -> Route to appropriate handler:       |
|      - "journal" -> Save to Qdrant        |
|      - "message" -> n8n chat workflow     |
|      - "note"    -> Save as note          |
|                                           |
|  /api/voice/status                        |
|    -> Return processing status            |
+------------------------------------------+
```

### 6.2 Audio Pipeline Flow

**Idle State (always running, minimal battery):**
1. `AudioRecord` captures 16kHz mono audio in 512-sample frames
2. Each frame goes through Porcupine (~0.5ms processing per frame)
3. If no wake word detected, frame is discarded immediately
4. Battery impact: ~15% additional drain (comparable to music playback)

**Active State (after wake word):**
1. Wake word "ydrasil [mode]" detected
2. Mode determines behavior:
   - **"ydrasil journal"** -- Record continuously, VAD segments speech, batch transcribe
   - **"ydrasil message"** -- Record until silence, send single message to chat
   - **"ydrasil stop"** -- Stop current recording session
3. Silero VAD segments audio into speech/silence
4. Speech segments encoded to Opus (24kbps)
5. Chunks sent to backend when WiFi/data available
6. Backend transcribes via Deepgram and processes via AI

### 6.3 Why Native Kotlin (Not Capacitor)

- **9x performance difference** for background audio processing tasks
- Direct access to `AudioRecord` API with minimal latency
- Native Porcupine SDK integration (no bridging)
- Native Silero VAD via `android-vad` library
- Full control over foreground service lifecycle
- No WebView overhead consuming memory/battery

If a web-based settings UI is desired, embed a local WebView as a secondary activity, or build a minimal Jetpack Compose UI.

### 6.4 Storage Requirements

| Audio Type | Bitrate | Per Hour | Per 8-Hour Day |
|-----------|---------|----------|----------------|
| Raw PCM 16kHz/16bit | 256 kbps | 115 MB | 920 MB |
| Opus (voice quality) | 24 kbps | 10.8 MB | 86 MB |
| Opus (after VAD filtering, ~25% speech) | 24 kbps | 2.7 MB | 22 MB |

With VAD filtering (keeping only speech), a full workday of recording is approximately **22 MB** -- negligible on modern phones.

### 6.5 Battery Life Expectations

- **Wake word only (idle):** ~15% additional battery drain over a full day
- **Active recording + VAD:** ~25-30% additional drain during active periods
- **With periodic API uploads:** Minimal additional impact if batched over WiFi
- **Total expected battery life:** A phone with 4500mAh should last 12-16 hours with the always-on listener running

### 6.6 Key Dependencies

```kotlin
// build.gradle.kts
dependencies {
    // Wake word
    implementation("ai.picovoice:porcupine-android:4.0.1")

    // Voice Activity Detection
    implementation("com.github.gkonovalov.android-vad:silero:1.0.0")

    // Audio encoding (Opus via Android MediaCodec or opus-android)
    // Network
    implementation("com.squareup.retrofit2:retrofit:2.9.0")

    // UI (minimal)
    implementation("androidx.compose.material3:material3:1.2.0")
}
```

### 6.7 Implementation Path (Phases)

**Phase 1: Proof of Concept (1-2 weeks)**
1. Create Android project with Kotlin + Jetpack Compose
2. Implement foreground service with `AudioRecord`
3. Integrate Porcupine with built-in wake word ("computer" or "jarvis") for testing
4. Add Silero VAD to detect speech segments
5. Save audio segments as Opus files locally
6. Test battery impact over a full day

**Phase 2: Backend Integration (1 week)**
1. Add FastAPI endpoints on VPS: `/api/voice/transcribe`, `/api/voice/process`
2. Integrate Deepgram Nova-3 for Danish transcription
3. Connect Android app to backend via Retrofit
4. Test end-to-end: wake word -> record -> transcribe -> display

**Phase 3: Custom Wake Words + Modes (1 week)**
1. Train custom "ydrasil" wake word via Picovoice Console
2. Implement multi-mode detection ("ydrasil journal", "ydrasil message")
3. Add mode-specific processing in backend
4. Integrate with existing n8n workflows and Qdrant

**Phase 4: Polish (1-2 weeks)**
1. Persistent notification with status indicator
2. Offline queue (record when no network, upload later)
3. Settings UI (wake word sensitivity, STT provider, modes)
4. Battery optimization tuning
5. Auto-restart after boot (user must open app once, then service persists)

### 6.8 Danish Wake Word Workaround

Since Porcupine does not officially support Danish, here is the recommended approach:

1. **Try "ydrasil" with the English model first.** The word has 3 syllables and distinct phonemes (/y/, /d/, /r/, /a/, /s/, /i/, /l/). Many of these exist in English. Test false positive/negative rates.
2. **Try the German model.** German phonology is closer to Danish (shared Nordic/Germanic roots). "Ydrasil" may work better.
3. **If neither works:** Contact Picovoice for commercial Danish support, or switch to OpenWakeWord with custom Danish TTS training.
4. **Simplest fallback:** Use an English-phonetic approximation like "ee-dra-sil" that is easier for English models to detect.

---

## Summary of Key Recommendations

| Component | Recommendation | Reason |
|-----------|---------------|--------|
| **Platform** | Native Android (Kotlin) | Performance, battery, direct API access |
| **Wake word** | Porcupine (Picovoice) | Best accuracy, easy setup, free tier |
| **VAD** | Silero VAD (android-vad lib) | Best accuracy, tiny model, MIT license |
| **STT** | Deepgram Nova-3 | Explicit Danish support, streaming, good price |
| **STT fallback** | GPT-4o Mini Transcribe | Cheapest batch option ($0.003/min) |
| **Audio codec** | Opus 24kbps | 10.8 MB/hour, excellent voice quality |
| **Backend** | FastAPI on existing VPS | Integrates with existing Qdrant + n8n infra |
| **AI processing** | Claude API via backend | Already in use in Ydrasil ecosystem |

Sources:
- [Porcupine Wake Word](https://picovoice.ai/platform/porcupine/)
- [Porcupine Android SDK](https://picovoice.ai/docs/quick-start/porcupine-android/)
- [OpenWakeWord](https://github.com/dscripka/openWakeWord)
- [OpenWakeWord Android Kotlin](https://github.com/Re-MENTIA/openwakeword-android-kt)
- [Android Foreground Service Types](https://developer.android.com/develop/background-work/services/fgs/service-types)
- [Android 14 FGS Changes](https://developer.android.com/about/versions/14/changes/fgs-types-required)
- [Android 15 FGS Changes](https://developer.android.com/about/versions/15/changes/foreground-service-types)
- [Silero VAD](https://github.com/snakers4/silero-vad)
- [Android VAD Library](https://github.com/gkonovalov/android-vad)
- [Deepgram Danish Support](https://deepgram.com/learn/deepgram-expands-nova-3-with-german-dutch-swedish-and-danish-support)
- [Deepgram Pricing](https://deepgram.com/pricing)
- [OpenAI Whisper Pricing](https://platform.openai.com/docs/pricing)
- [Whisper Danish Fine-tuning](https://medium.com/@rasgaard/fine-tuning-whisper-tiny-for-danish-for-free-c77f4dac9d94)
- [Google Chirp 3](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3)
- [AssemblyAI Pricing](https://www.assemblyai.com/pricing)
- [ONNX Whisper on Android](https://github.com/microsoft/onnxruntime-inference-examples/blob/main/mobile/examples/whisper/local/android/readme.md)
- [Capawesome Audio Recorder](https://capawesome.io/plugins/audio-recorder/)
- [OVOS](https://www.openvoiceos.org/)
- [Notely Voice on F-Droid](https://f-droid.org/en/packages/com.module.notelycompose.android/)
- [Scriberr](https://github.com/rishikanthc/Scriberr)
- [Picovoice Pricing](https://picovoice.ai/pricing/)
- [Opus Codec](https://opus-codec.org/)
