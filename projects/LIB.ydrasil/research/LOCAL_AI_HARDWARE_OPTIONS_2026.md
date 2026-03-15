# Lokal AI Hardware: Komplet Guide (Februar 2026)

**For:** Kris (ikke-teknisk bruger, chauffar i Danmark)
**Opdateret:** 2026-02-11
**Formaal:** Oversigt over hvad du kan kobe, hvad det koster, og hvad det kan.

---

## TL;DR — Hurtig Anbefaling

| Behov | Anbefaling | Pris | Vigtigste fordel |
|-------|-----------|------|-----------------|
| **Bedste for begyndere** | Mac Mini M4 Pro 64GB | ~21.300 DKK | Stille, lav strom, korer 32B-modeller hurtigt |
| **Bedste pris/ydelse** | Brugt PC + RTX 3090 | ~8.000-10.000 DKK | 24GB VRAM, korer 32B-modeller, Whisper, TTS |
| **Bedste til 70B modeller** | Beelink GTR9 Pro (128GB) | ~14.800 DKK | Korer 70B lokalt, kompakt, stille |
| **Billigste start** | Cloud GPU (RunPod) | ~2,5 DKK/time | Ingen hardware-investering |
| **Anbefales IKKE** | Jetson Orin Nano | ~1.900 DKK | For lille til serioese LLM-modeller |

---

## 1. Mac Mini M4 Pro (64GB)

### Pris
- **Apple Danmark (apple.com/dk):** 21.299 DKK (M4 Pro, 14-core CPU, 20-core GPU, 64GB, 512GB SSD)
- **Med 1TB SSD:** ca. 23.800 DKK
- **Med 2TB SSD:** ca. 28.800 DKK
- I EUR: ca. 2.860 EUR

### Specifikationer
- **RAM (unified memory):** 24GB / 48GB / 64GB — vaelg 64GB til LLM-brug
- **Memory bandwidth:** 273 GB/s (M4 Pro) — dette er flaskehalsen for LLM-hastighed
- **GPU:** 20-core integreret GPU — deler hukommelse med CPU
- **Strom:** 3,5W idle, 50-60W under LLM-belastning, max 155W
- **Storrelse:** 12,7 x 12,7 cm — lille nok til et skrivebord

### LLM-ydelse (tokens/sekund)

| Model | Storrelse | Kvantisering | Hastighed | Brugbar? |
|-------|----------|-------------|-----------|----------|
| Llama 3.2 1B | 1B | Q4 | ~95-100 t/s | Lynhurtigt |
| Phi-3.5 / Gemma 2 9B | 8-9B | Q4 | ~28-30 t/s | Meget godt |
| Qwen 2.5 14B | 14B | Q4 | ~20-22 t/s | Godt |
| Gemma 2 27B | 27B | Q4 | ~8-10 t/s | Langsomt men brugbart |
| Qwen 2.5 32B | 32B | Q4 | ~10-12 t/s | Brugbart |
| Llama 3.3 70B | 70B | Q4 | ~4-6 t/s | For langsomt til daglig brug |

### Whisper (tale-til-tekst)
- Whisper Large v3 Turbo via MLX: 10 min lyd transskriberes paa ~60 sekunder
- WhisperKit (Apple-optimeret): ~0,45 sekunder latency for streaming
- **Vurdering: Fremragende til Whisper**

### TTS (tekst-til-tale)
- Kokoro TTS korer fint paa CPU — 3-11x realtid
- Piper TTS korer endnu hurtigere paa CPU
- **Vurdering: Fungerer godt**

### Fordele
- Ekstremt lavt stroemforbrug (50-60W under brug vs. 400-600W for GPU-PC)
- Helt lydlos under normal brug
- macOS "just works" med Ollama — installer og koer
- Ingen separat GPU nødvendig — unified memory bruges til alt

### Ulemper
- 64GB er maks — kan ikke opgraderes
- Dyrt for hvad du faar (21.300 DKK)
- 70B modeller er for langsomme
- Lavere memory bandwidth end M4 Max (273 vs. 546 GB/s)

### Vigtig note om bandwidth
M4 Pro har 273 GB/s memory bandwidth. En aeldre M3 Max har 400 GB/s og genererer tokens *hurtigere* selvom M4 Pro er nyere. For LLM-brug er bandwidth vigtigere end chip-generation.

---

## 2. Brugt Gaming-PC med NVIDIA RTX 3090 eller 4090

### RTX 3090 (24GB VRAM)

#### Pris
- **Brugt (eBay Europa):** ~630 EUR / ~4.700 DKK (februar 2026)
- **Komplet PC med brugt RTX 3090:** ~8.000-10.000 DKK

Eksempel-build med brugte dele:

| Komponent | Pris (ca.) |
|-----------|-----------|
| RTX 3090 (brugt) | 4.700 DKK |
| AMD Ryzen 5 5600X + bundkort + 32GB RAM | 2.500 DKK |
| 1TB NVMe SSD | 500 DKK |
| 850W PSU (80+ Gold) | 800 DKK |
| Kabinet | 500 DKK |
| **Total** | **~9.000 DKK** |

#### Hvad kan den koere?

| Model | Storrelse | Kvantisering | Passer i 24GB? | Hastighed |
|-------|----------|-------------|----------------|-----------|
| Llama 3 8B | 8B | Q4 (4-bit) | Ja (5GB) | ~100-140 t/s |
| Mistral 7B | 7B | Q4 | Ja (5GB) | ~100-130 t/s |
| Qwen 2.5 14B | 14B | Q4 | Ja (10GB) | ~60-80 t/s |
| DeepSeek R1 Distill 32B | 32B | Q4 | Ja (~18GB) | ~30-40 t/s |
| Llama 3.3 70B | 70B | Q4 | NEJ (35GB) — kraever offload | ~8-15 t/s (langsomt) |

**Konklusion:** RTX 3090 er fantastisk til modeller op til 32B. 70B kraever offloading til system-RAM og bliver langsomt.

#### Strom og stoj
- **GPU alene:** 350-450W under belastning
- **Hele systemet:** 500-700W under belastning
- **Stoj:** Hojt — GPU-blaesere korer paa fuldt blus

### RTX 4090 (24GB VRAM)

#### Pris
- **Brugt (eBay Europa):** ~2.160 EUR / ~16.100 DKK (februar 2026)
- **Komplet PC:** ~22.000-26.000 DKK

#### Ydelse

| Model | Hastighed |
|-------|-----------|
| 8B modeller | ~140-150 t/s |
| 32B modeller | ~30-40 t/s |
| 70B (med offload) | ~40-52 t/s (med TensorRT-LLM optimering) |

#### Strom
- **GPU alene:** 400-450W TDP, spikes op til 600W
- **Hele systemet:** 600-800W under belastning
- **Anbefalet PSU:** Minimum 1000W

#### Vurdering
RTX 4090 er ~16% hurtigere end RTX 3090 til LLM-inference, men koster 3,4x mere brugt. **RTX 3090 er langt bedre pris/ydelse.**

Artiklen "A used RTX 3090 remains the value king for local AI" opsummerer det godt.

---

## 3. AI Mini-PC: Beelink GTR9 Pro

### Specifikationer
- **Processor:** AMD Ryzen AI Max+ 395 (12 cores, 24 threads)
- **RAM:** 128GB LPDDR5X (hvoraf 96GB kan bruges som GPU-VRAM)
- **NPU:** 50 TOPS dedikeret neural processor
- **Total AI performance:** 126 TOPS
- **Memory bandwidth:** ~212 GB/s (maalt), 256 GB/s (teoretisk)
- **Strom:** ~140W max TDP
- **Storrelse:** Mac Studio-lignende formfaktor

### Pris
- **Beelink.com / Amazon:** ~1.985 USD / ~14.800 DKK
- Inkluderer 128GB RAM + 2TB SSD

### LLM-ydelse

| Model | Hastighed |
|-------|-----------|
| 8B modeller | Hurtigt (estimeret 40-60 t/s) |
| 32B modeller | Brugbart (estimeret 15-25 t/s) |
| 70B modeller (Q4) | ~3-10 t/s (langsomt — tidlig ROCm-support) |
| Phi-3.5 | ~61 t/s (bekraeftet benchmark) |

### Fordele
- **128GB RAM = kan loade 70B modeller fuldt i hukommelsen** — ingen offloading
- Kompakt og relativt stille
- Dobbelt 10GbE netvaerk
- Lavt stroemforbrug (140W vs. 700W for GPU-PC)

### Ulemper
- **ROCm driver-support er ufuldstaendig** — Linux kraeves for bedste ydelse
- Langsommere end dedikeret NVIDIA GPU til selve beregningen
- Nyt produkt — faa community-benchmarks endnu
- 14.800 DKK er dyrt for usikker ydelse

### Vurdering
Spaendende koncept. Kan koere 70B modeller i hukommelsen, men hastigheden er endnu ikke paa niveau med NVIDIA GPUer. Vent 3-6 maaneder paa bedre driver-support og benchmarks.

---

## 4. Cloud GPU Rental

### Priser (februar 2026)

| Udbyder | GPU | Pris/time (USD) | Pris/time (DKK) |
|---------|-----|----------------|-----------------|
| **RunPod (community)** | RTX 4090 | $0.34 | ~2,5 DKK |
| **RunPod (community)** | RTX A6000 | $0.33 | ~2,5 DKK |
| **RunPod (community)** | H100 | $1.99 | ~14,8 DKK |
| **Vast.ai (marketplace)** | H100 | $1.87 | ~13,9 DKK |
| **Lambda Labs** | H100 | $2.99 | ~22,3 DKK |

### Maanedlig omkostning (altid-taaendt, 730 timer)

| Udbyder | GPU | Maanedlig (DKK) |
|---------|-----|-----------------|
| RunPod | RTX 4090 | ~1.850 DKK |
| RunPod | H100 | ~10.800 DKK |
| Vast.ai | H100 | ~10.100 DKK |

### Maanedlig omkostning (4 timer/dag, 120 timer)

| Udbyder | GPU | Maanedlig (DKK) |
|---------|-----|-----------------|
| RunPod | RTX 4090 | ~300 DKK |
| RunPod | H100 | ~1.780 DKK |

### Fordele
- Ingen hardware-investering
- Adgang til kraftige GPUer (H100) du aldrig ville kobe selv
- Skalerer op/ned efter behov

### Ulemper
- **Lobende omkostning** — loeser sig aldrig
- Internetforbindelse kraeves
- Data forlader din maskine
- Latency (netvaerk + opstart)

### Vurdering
Cloud GPU giver mening til eksperimentering og lejlighedsvis brug. Hvis du bruger det >4 timer/dag, er hardware billigere indenfor 6-12 maaneder.

**Break-even beregning:**
- RunPod RTX 4090 a 2,5 DKK/time x 4 timer/dag x 365 dage = 3.650 DKK/aar
- Brugt RTX 3090 koster 4.700 DKK = tjent hjem paa ~15 maaneder
- Mac Mini M4 Pro 64GB koster 21.300 DKK = tjent hjem paa ~6 aar

---

## 5. NVIDIA Jetson Orin Nano Super

### Pris
- **Officiel:** 249 USD / ~1.900 DKK
- Halveret fra original pris paa 499 USD

### Specifikationer
- **GPU:** Ampere-arkitektur, 67 TOPS AI-ydelse
- **RAM:** 8GB LPDDR5 (delt mellem CPU og GPU)
- **Strom:** 5-25W (justerbar)

### LLM-kapabilitet
- **8B modeller:** Langsomt men muligt (Llama 3.2 3B bedre egnet)
- **32B+ modeller:** Umuligt — kun 8GB RAM
- **Bedst til:** Smaa modeller (1B-4B), Phi-3, Gemma 3B

### Whisper
- Kan koere Whisper-modeller, men kun tiny/base med rimelig hastighed
- Large-modeller passer ikke i 8GB RAM

### TTS
- Kan koere Piper TTS (letvaegtigt)
- Kokoro TTS muligt men langsomt

### Strom
- 5-25W — ekstremt lavt

### Vurdering
**Anbefales IKKE til LLM-brug.** 8GB RAM er for lidt. Jetson er designet til robotik, billedgenkendelse og edge-computing — ikke til at koere store sprogmodeller. For de ~1.900 DKK faar du mere ved at laegge dem til side mod en Mac Mini.

---

## 6. Ollama — Hvad er det?

### Kort forklaring
Ollama er et gratis program der goer det nemt at koere AI-modeller lokalt. Taenk paa det som "App Store for AI-modeller" — du skriver een kommando og modellen downloades og korer.

### Sadan virker det
```bash
# Installer (Mac, Linux, Windows)
curl -fsSL https://ollama.com/install.sh | sh

# Download og koer en model
ollama pull llama3.3:70b
ollama run llama3.3:70b

# Eller en mindre model
ollama run qwen2.5:14b
```

Det er det. Ingen Python, ingen konfiguration, ingen GPU-drivers at rode med.

### Tilgaengelige modeller (februar 2026)
Ollama har 100+ modeller. De vigtigste:

| Model | Storrelser | Bemaekning |
|-------|-----------|------------|
| **Llama 3.3** | 70B | Metas nyeste, staerkt generelt |
| **Llama 3.2** | 1B, 3B | Smaa, hurtige |
| **Llama 4** | Flere varianter | Nyeste fra Meta |
| **Qwen 2.5** | 0.5B - 72B | Alibaba, staerkt til kode og matematik |
| **Qwen 3** | Flere varianter | Nyeste generation med MoE |
| **DeepSeek R1** | 1.5B - 671B (distill: 8B-70B) | Bedst til raesonnering |
| **Mistral** | 7B, 8x7B, 8x22B, Small 3 | Effektive, gode generalister |
| **Gemma 2** | 2B, 9B, 27B | Google, gode smaa modeller |
| **Phi-3/4** | 3.8B, 14B | Microsoft, overraskende gode for stoerrelsen |
| **Kokoro TTS** | - | Tekst-til-tale |
| **Whisper** | Flere storrelser | Tale-til-tekst |

### Ollamas fordele
- En-kommando installation
- Automatisk GPU-detektion (NVIDIA, AMD, Apple Silicon)
- Automatisk kvantisering (vaelger bedste format til din hardware)
- REST API (nemt at integrere med andre programmer)
- Korer paa Mac, Linux og Windows

---

## 7. Bedste Open-Source Modeller (Februar 2026)

### Oversigt med styrker

| Model | Bedst til | Hvorfor |
|-------|----------|---------|
| **Llama 3.3 70B** | Generelt, instruktionsfolgning, struktureret output | Balanceret, god til alt |
| **Qwen 2.5 72B** | Kode, matematik, forskning | Scorer hoejest paa MATH (83,1) og LiveCodeBench (55,5) |
| **DeepSeek R1** | Raesonnering, logik, forklaring | Viser sin tankeproces, 73% af akademiske papers bruger den |
| **Mistral Small 3** | Effektivitet, daglig brug, 24GB GPUer | Sweet spot for pris/ydelse, passer i 14-15GB Q4 |
| **Gemma 2 27B** | Kompakt styrke | God til 32GB+ systemer |
| **Phi-3.5 / Phi-4** | Smaa enheder, hurtig inference | Overraskende god for 3.8-14B parametre |
| **Qwen 3** | Nyeste MoE-modeller | Slaer Mistral Large paa AIME25 (92,3% vs 75%) |

### Praktisk anbefaling efter hardware

| Din hardware | Bedste model | Alternativ |
|-------------|-------------|------------|
| **8GB RAM / ingen GPU** | Phi-3 Mini (3.8B) | Gemma 2B |
| **16GB RAM / ingen GPU** | Llama 3 8B, Qwen 2.5 7B | Mistral 7B |
| **24GB VRAM (RTX 3090)** | DeepSeek R1 Distill 32B, Mistral Small 3 | Qwen 2.5 32B |
| **48-64GB unified (Mac)** | Qwen 2.5 32B, Llama 3.3 70B (langsomt) | DeepSeek R1 Distill 32B |
| **96-128GB (GTR9 Pro)** | Llama 3.3 70B, Qwen 2.5 72B | DeepSeek R1 |

### DeepSeek R1 Distill-varianter (saeligt interessante)
DeepSeek har destilleret deres store R1-model ned til mindre versioner:

| Variant | Base-model | Storrelse | Ydelse |
|---------|-----------|----------|--------|
| R1-Distill-Qwen-1.5B | Qwen 2.5 | 1.5B | God til simple opgaver |
| R1-Distill-Llama-8B | Llama 3.1 | 8B | ~17 t/s paa CPU med NPU |
| R1-Distill-Qwen-14B | Qwen 2.5 | 14B | God balance |
| R1-Distill-Qwen-32B | Qwen 2.5 | 32B | **Slaer OpenAI o1-mini** |
| R1-Distill-Llama-70B | Llama 3.1 | 70B | Naer fuld R1-kvalitet |

**R1-Distill-Qwen-32B er den mest interessante** — den slaer OpenAI o1-mini paa benchmarks og korer paa en RTX 3090 med Q4.

---

## 8. Whisper (tale-til-tekst) — Lokal Performance

### Hvad er Whisper?
OpenAIs automatiske talegenkendelse. Open-source, gratis, korer lokalt. Forstaar 100+ sprog inklusive dansk.

### Hastighed efter hardware

| Hardware | Model | 10 min lyd | Realtidsfaktor |
|----------|-------|-----------|----------------|
| **RTX 4090** | Large v3 | ~30 sek | ~20x realtid |
| **RTX 3090** | Large v3 | ~36 sek | ~17x realtid |
| **Mac M4 Pro** | Large v3 Turbo (MLX) | ~60 sek | ~10x realtid |
| **Mac M4 Pro** | WhisperKit (streaming) | ~0,45s latency | Realtid |
| **CPU-only (VPS)** | Tiny/Base | ~2-5 min | ~2-5x realtid |
| **Jetson Orin Nano** | Tiny/Base | ~3-8 min | ~1-3x realtid |

### Modeller

| Model | Parametre | VRAM | Kvalitet |
|-------|----------|------|---------|
| Tiny | 39M | ~1GB | Basis — fejl i dansk |
| Base | 74M | ~1GB | Bedre, stadig fejl |
| Small | 244M | ~2GB | God til de fleste sprog |
| Medium | 769M | ~5GB | Meget god |
| Large v3 | 1.5B | ~10GB | Bedste kvalitet |
| Large v3 Turbo | 809M | ~6GB | **Anbefalet: naesten lige saa god som Large, 5x hurtigere** |

### Vurdering
Whisper korer fremragende lokalt paa alle platforme undtagen Jetson. **Large v3 Turbo er den anbefalede model** — naesten identisk kvalitet med Large v3, men 5x hurtigere.

---

## 9. TTS (tekst-til-tale) — Lokale Muligheder

### Kokoro TTS
- **Parametre:** 82M (ekstremt lille)
- **Licens:** Apache 2.0 (helt gratis)
- **Hastighed:** 3-11x realtid paa CPU
- **Kvalitet:** Sammenlignelig med modeller 5-15x stoerre
- **Sprog:** Engelsk (US/UK), Fransk, Koreansk, Japansk, Mandarin, Hindi, Spansk, Italiensk, Portugisisk
- **Dansk:** NEJ — ikke understottet
- **Koerer paa CPU:** Ja, med ONNX-runtime

### Piper TTS
- **Type:** Letvaegtigt, designet til edge/embeddede enheder
- **Hastighed:** Hurtigere end realtid, selv paa CPU
- **Dansk:** JA — stemmen "talesyntese" (medium kvalitet) er tilgaengelig
- **Kvalitet:** Funktionel men lidt robotisk sammenlignet med Kokoro
- **Bruges af:** Home Assistant, OpenVoiceOS

### XTTS-v2 (Coqui)
- **Type:** Neural TTS med voice cloning
- **Sprog:** 17 sprog — **dansk er IKKE inkluderet**
- **Kvalitet:** Hoj — naturligt klingende
- **Note:** Coqui AI lukkede i december 2025, men open-source koden lever videre

### Anbefaling for dansk TTS
- **Piper TTS med "talesyntese"** er den eneste brugbare open-source mulighed for dansk
- Kvaliteten er "OK" — brugbar til notifikationer og simple beskeder
- For hoj-kvalitets dansk tale er cloud-TTS (Google, Azure, ElevenLabs) stadig overlegen

---

## 10. Stroemforbrug — Sammenligning

| Hardware | Idle | Under LLM-brug | Maanedlig strom (4 timer/dag) | Aarlig strom |
|----------|------|----------------|------------------------------|-------------|
| **Mac Mini M4 Pro** | 3,5W | 50-60W | ~7 kWh / ~17 DKK | ~80 kWh / ~200 DKK |
| **PC + RTX 3090** | 80-100W | 500-600W | ~73 kWh / ~182 DKK | ~876 kWh / ~2.190 DKK |
| **PC + RTX 4090** | 80-100W | 600-800W | ~95 kWh / ~237 DKK | ~1.140 kWh / ~2.850 DKK |
| **Beelink GTR9 Pro** | 15-25W | 100-140W | ~17 kWh / ~43 DKK | ~204 kWh / ~510 DKK |
| **Jetson Orin Nano** | 5W | 15-25W | ~3 kWh / ~8 DKK | ~36 kWh / ~90 DKK |

*(Beregnet med dansk elpris ca. 2,50 DKK/kWh inkl. afgifter)*

---

## 11. Samlet Sammenligning

| Kriterium | Mac Mini M4 Pro 64GB | PC + RTX 3090 | Beelink GTR9 Pro | Cloud (RunPod) | Jetson Orin Nano |
|-----------|---------------------|---------------|------------------|----------------|-----------------|
| **Pris** | 21.300 DKK | ~9.000 DKK | ~14.800 DKK | ~300 DKK/md (4t/dag) | ~1.900 DKK |
| **8B model** | 28-30 t/s | 100-140 t/s | 40-60 t/s | 140-150 t/s | Langsomt |
| **32B model** | 10-12 t/s | 30-40 t/s | 15-25 t/s | 30-40 t/s | Umuligt |
| **70B model** | 4-6 t/s | Langsomt (offload) | 3-10 t/s | 40-52 t/s | Umuligt |
| **Whisper** | Fremragende | Fremragende | God | Fremragende | Kun smaa modeller |
| **Dansk TTS** | Piper (OK) | Piper (OK) | Piper (OK) | Piper (OK) | Piper (OK) |
| **Strom** | 50-60W | 500-700W | 100-140W | 0W (hos dem) | 15-25W |
| **Stoj** | Stille | Hojt | Lavt | N/A | Stille |
| **Svaerhedsgrad** | Nemt | Mellemsvart | Mellemsvart | Nemt | Svart |
| **Offline?** | Ja | Ja | Ja | Nej | Ja |

---

## 12. Min Anbefaling til Kris

### Hvis du vil starte NU (0 DKK)
1. Installer Ollama paa VPS'en (den du allerede har)
2. Koer `ollama pull phi3:mini` — korer paa CPU
3. Test det. Forstaa hvordan det virker
4. Brug fortsat Claude API til det vigtige

### Hvis du vil investere smart (9.000 DKK)
**Brugt gaming-PC med RTX 3090:**
- Find en brugt RTX 3090 paa DBA.dk eller eBay (~4.700 DKK)
- Byg/koeb resten brugt (~4.300 DKK)
- Installer Ollama + DeepSeek R1 Distill 32B
- Korer 32B modeller paa 30-40 t/s — hurtigere end Claude-svar
- Whisper Large v3 Turbo transkriberer 10 min paa 36 sek
- **Bedste pris/ydelse**

### Hvis du vil have det nemt og stille (21.300 DKK)
**Mac Mini M4 Pro 64GB:**
- Koeb paa apple.com/dk
- Installer Ollama (et klik)
- Koer 32B modeller komfortabelt
- Stille, lavt stroemforbrug, paent
- Fungerer ogsaa som normal computer

### Hvad du IKKE skal goere
- Koeb IKKE en Jetson Orin Nano til LLM-brug (for lidt RAM)
- Koeb IKKE en RTX 4090 (brugt 16.100 DKK for 16% mere ydelse end 3090)
- Koeb IKKE "altid-taaendt" cloud GPU (det lober op)
- Vent med Beelink GTR9 Pro til driver-support er bedre (3-6 maaneder)

---

## Kilder

- [Mac Mini M4 Pro — Apple Danmark](https://www.apple.com/dk/shop/buy-mac/mac-mini)
- [Mac Mini M4 Pro LLM Benchmarks — MacRumors](https://forums.macrumors.com/threads/so-happy-with-the-m4-pro-i-can-finally-use-ai-stuff-locally.2442964/)
- [M4 Max LLM Performance — Sean Vosler / Medium](https://seanvosler.medium.com/the-200b-parameter-cruncher-macbook-pro-exploring-the-m4-max-llm-performance-8fd571a94783)
- [M4 Mac Mini Power Efficiency — Jeff Geerling](https://www.jeffgeerling.com/blog/2024/m4-mac-minis-efficiency-incredible)
- [RTX 3090 Value King for Local AI — XDA Developers](https://www.xda-developers.com/used-rtx-3090-value-king-local-ai/)
- [RTX 3090 Local LLMs Guide — Hardware Corner](https://www.hardware-corner.net/guides/rtx-3090-local-llms-24gb-vram/)
- [RTX 4090 Ollama Benchmarks — DatabaseMart](https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx4090)
- [GPU Ranking for LLMs — Hardware Corner](https://www.hardware-corner.net/gpu-ranking-local-llm/)
- [Best GPU for AI 2025 — Local AI Master](https://localaimaster.com/blog/best-gpus-for-ai-2025)
- [RTX 4090 Price Tracker EU](https://bestvaluegpu.com/en-eu/history/new-and-used-rtx-4090-price-history-and-specs/)
- [RTX 3090 Price Tracker EU](https://bestvaluegpu.com/en-eu/history/new-and-used-rtx-3090-price-history-and-specs/)
- [Beelink GTR9 Pro Review — ServeTheHome](https://www.servethehome.com/beelink-gtr9-pro-review-amd-ryzen-ai-max-395-system-with-128gb-and-dual-10gbe/)
- [Beelink GTR9 Pro — Hardware Corner](https://www.hardware-corner.net/llm-mini-pc-beelink-gtr9-pro-unveiled/)
- [Strix Halo LLM Benchmarks — Level1Techs](https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796)
- [Strix Halo GPU LLM Tests — Framework Community](https://community.frame.work/t/amd-strix-halo-ryzen-ai-max-395-gpu-llm-performance-tests/72521)
- [Jetson Orin Nano Super — NVIDIA](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/)
- [Jetson Edge AI Getting Started — NVIDIA Blog](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/)
- [RunPod Pricing](https://www.runpod.io/pricing)
- [Vast.ai Pricing](https://vast.ai/pricing)
- [Cloud GPU Rental Platforms 2026 — Hyperstack](https://www.hyperstack.cloud/blog/case-study/cloud-gpu-rental-platforms)
- [Ollama Model Library](https://ollama.com/library)
- [Top Open Source LLMs 2026 — HuggingFace](https://huggingface.co/blog/daya-shankar/open-source-llms)
- [Open Source LLM Comparison — Vahu.org](https://vahu.org/selecting-open-source-llms-llama-mistral-qwen-and-deepseek-compared)
- [Qwen 2.5 72B vs Llama 3.3 70B — Novita AI](https://blogs.novita.ai/qwen-2-5-72b-vs-llama-3-3-70b-which-model-suits-your-needs/)
- [Whisper GPU Benchmarks — Tom's Hardware](https://www.tomshardware.com/news/whisper-audio-transcription-gpus-benchmarked)
- [Whisper on Apple Silicon — Voicci](https://www.voicci.com/blog/apple-silicon-whisper-performance.html)
- [Whisper Large v3 Turbo — Whisper Notes](https://whispernotes.app/blog/introducing-whisper-large-v3-turbo)
- [Kokoro TTS](https://kokorottsai.com/)
- [Open Source TTS Models 2026 — BentoML](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [Piper TTS Danish Voice — GitHub](https://github.com/rhasspy/piper/blob/master/VOICES.md)
- [XTTS Multilingual TTS — Medium](https://medium.com/machine-learns/xtts-open-source-tts-in-13-languages-e05c19782a03)
- [Best Mini PCs for AI Server 2026 — PC Build Advisor](https://www.pcbuildadvisor.com/best-mini-pcs-for-ai-server-the-ultimate-server-mini-pcs-for-2026-new-models-included/)
- [DeepSeek R1 — GitHub](https://github.com/deepseek-ai/DeepSeek-R1)
