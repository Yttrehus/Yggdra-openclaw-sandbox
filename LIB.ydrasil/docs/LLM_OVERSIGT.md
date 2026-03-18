# Comprehensive AI/LLM Model Comparison -- January 2026

## 1. All Major Providers and Model Lineups

### OpenAI
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **GPT-5.2** | $1.50 | $10.00 | 400K | Flagship |
| **GPT-5** | $1.25 | $10.00 | 400K | Flagship |
| **GPT-5 Mini** | $0.25 | $2.00 | 400K | Mid-tier |
| **GPT-5 Nano** | $0.05 | $0.40 | 400K | Budget |
| **GPT-4.1** | $2.00 | $8.00 | 1M | General purpose |
| **GPT-4.1 Mini** | $0.40 | $1.60 | 1M | Mid-tier |
| **GPT-4.1 Nano** | $0.10 | $0.40 | 1M | Budget |
| **GPT-4o** | $2.50 | $10.00 | 128K | Legacy flagship |
| **GPT-4o Mini** | $0.15 | $0.60 | 128K | Legacy budget |
| **o3** | $0.40 | $1.60 | 200K | Reasoning |
| **o4-mini** | $1.10 | $4.40 | 200K | Reasoning (compact) |
| text-embedding-3-small | $0.02 | -- | 8K | Embeddings |
| text-embedding-3-large | $0.13 | -- | 8K | Embeddings |

**Notes:** o3 received an 80% price cut in mid-2025. Reasoning models bill "thinking tokens" as output tokens. Batch API available at 50% off for most models.

---

### Anthropic (Claude)
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **Claude Opus 4.5** | $5.00 | $25.00 | 200K | Flagship reasoning |
| **Claude Sonnet 4.5** | $3.00 | $15.00 | 200K (1M beta) | Balanced |
| **Claude Haiku 4.5** | $1.00 | $5.00 | 200K | Fast/cheap |
| Claude 3 Haiku (legacy) | $0.25 | $1.25 | 200K | Budget legacy |

**Notes:** Sonnet 4.5 long-context (>200K) costs $6.00/$22.50. Batch API at 50% off. Prompt caching: reads at 0.1x base price. Extended thinking tokens billed as output.

---

### Google (Gemini)
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **Gemini 3 Pro Preview** | $2.00 | $12.00 | 1M | Flagship reasoning |
| **Gemini 2.5 Pro** | $1.25 | $10.00 | 1M | Strong general |
| **Gemini 2.5 Flash** | $0.15 | $0.60 | 1M | Fast balanced |
| **Gemini 2.5 Flash-Lite** | $0.10 | $0.40 | 1M | Budget |
| **Gemini 2.0 Flash-Lite** | $0.075 | $0.30 | 1M | Cheapest |
| gemini-embedding-001 | ~$0.00 | -- | -- | Embeddings (free tier) |

**Notes:** Gemini 3 Pro >200K context doubles pricing to $4.00/$18.00. Free tier available for all models. Context caching cuts costs up to 75%.

---

### xAI (Grok)
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **Grok 4** | $3.00 | $15.00 | 131K (2M avail) | Flagship reasoning |
| **Grok 4.1 Fast** | $0.20 | $0.50 | 131K | Fast/cheap |
| **Grok 3** | $3.00 | $15.00 | 131K | Legacy |
| **Grok 3 Mini** | $0.30 | $0.50 | 131K | Legacy budget |
| **Grok Code Fast 1** | $0.20 | $0.50 | 131K | Coding specialized |

**Notes:** Large context (>131K) doubles pricing to $6.00/$30.00. Server-side tools (web search, code execution) cost $2.50-$5.00 per 1,000 calls.

---

### DeepSeek
| Model | Input/1M | Output/1M | Context | Type | License |
|---|---|---|---|---|---|
| **DeepSeek V3.2 Exp** | $0.021 | $0.32 | 128K | General | MIT |
| **DeepSeek V3.1** | $0.15 | $0.75 | 128K | General | MIT |
| **DeepSeek R1** | $0.70 | $2.40 | 164K | Reasoning | MIT |
| **DeepSeek R1 0528** | $0.45 | $2.15 | 164K | Reasoning | MIT |
| **DeepSeek Prover V2** | $0.50 | $2.18 | 128K | Math proofs | MIT |
| R1 Distill Llama 70B | $0.03 | $0.11 | 128K | Distilled | MIT |

**Notes:** Cache hits reduce input costs by ~75%. All models open-source (MIT license) and self-hostable for zero API cost.

---

### Meta (Llama) -- via hosting providers
| Model | Input/1M | Output/1M | Context | Provider | License |
|---|---|---|---|---|---|
| **Llama 4 Maverick** (400B MoE, 17B active) | $0.22 | $0.88 | 1M | Fireworks | Open |
| **Llama 4 Maverick** | $0.27 | $0.85 | 1M | Together | Open |
| **Llama 4 Scout** (109B MoE, 17B active) | $0.15 | $0.60 | 10M | Fireworks | Open |
| **Llama 4 Scout** | $0.18 | $0.59 | 10M | Together | Open |

**Notes:** Llama 4 Scout has the largest context window of any model (10M tokens). Meta's open-weight models are free to self-host. Pricing varies by hosting provider.

---

### Mistral AI
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **Mistral Large 3** (675B MoE) | $0.50 | $1.50 | 128K | Flagship |
| **Mistral Medium 3.1** | $0.40 | $2.00 | 128K | Balanced |
| **Codestral 2508** | $0.30 | $0.90 | 32K | Coding |
| **Devstral Medium** | $0.40 | $2.00 | 128K | Coding |
| **Mistral Small 3.2** (24B) | $0.06 | $0.18 | 128K | Budget |
| **Devstral Small** | $0.06 | $0.12 | 128K | Budget coding |
| **Mistral Nemo** | $0.02 | $0.06 | 128K | Cheapest |

**Notes:** Multiple models are open-weight. Codestral specialized for 80+ programming languages.

---

### Cohere
| Model | Input/1M | Output/1M | Context | Type |
|---|---|---|---|---|
| **Command A** | $2.50 | $10.00 | 256K | Flagship |
| **Command R+** | $2.50 | $10.00 | 128K | Strong general |
| **Command R** | $0.15 | $0.60 | 128K | Budget |
| **Command R7B** | $0.0375 | $0.15 | 128K | Cheapest |
| **Embed v4** | $0.12/1M | -- | -- | Multimodal embeddings |
| **Rerank 3.5** | $2.00/1K searches | -- | -- | Reranking |

**Notes:** Cohere is uniquely strong in enterprise RAG with dedicated reranking models. Embed v4 supports images.

---

### Alibaba (Qwen)
| Model | Input/1M | Output/1M | Context | Type | License |
|---|---|---|---|---|---|
| **Qwen3-235B-A22B** | $0.20-$1.20 | $1.00-$6.00 | 256K (1M ext.) | Flagship MoE | Open |
| **Qwen3-32B** | $0.15 | $0.75 | 128K | Dense | Open |
| **Qwen 2.5-Max** | $0.38 | ~$1.50 | 128K | General | Open |

**Notes:** Available via Alibaba Cloud, OpenRouter, and Groq. Supports both thinking and non-thinking modes. All open-weight.

---

### Other Notable Models
| Model | Provider | Input/1M | Output/1M | Context | Notes |
|---|---|---|---|---|---|
| **GLM-4.7 Thinking** | Zhipu AI | Free self-host | -- | 128K | 89% LiveCodeBench (matches GPT-5.2) |
| **Kimi-K2-Instruct** | Moonshot | ~$0.20 | ~$1.00 | 128K | Top agentic/tool-use performance |
| **Doubao-Seed-1.8** | ByteDance | ~$0.30 | ~$1.50 | 128K | Leads LiveCodeBench at 75% |

---

## 2. Pricing Tiers Summary (Input/Output per 1M tokens)

### Ultra-Budget Tier (< $0.10 input)
| Model | Input | Output | Best For |
|---|---|---|---|
| DeepSeek V3.2 Exp | $0.021 | $0.32 | General tasks at lowest cost |
| Mistral Nemo | $0.02 | $0.06 | Simple classification |
| GPT-5 Nano | $0.05 | $0.40 | Fast simple tasks |
| Mistral Small 3.2 | $0.06 | $0.18 | Budget European option |
| Gemini 2.0 Flash-Lite | $0.075 | $0.30 | Cheapest Google option |
| Cohere Command R7B | $0.0375 | $0.15 | Budget RAG |

### Budget Tier ($0.10 - $0.50 input)
| Model | Input | Output | Best For |
|---|---|---|---|
| GPT-4o Mini | $0.15 | $0.60 | Cheap OpenAI tasks |
| Gemini 2.5 Flash | $0.15 | $0.60 | Balanced speed/cost |
| DeepSeek V3.1 | $0.15 | $0.75 | Open-source general |
| Llama 4 Scout | $0.15 | $0.60 | 10M context, open |
| GPT-5 Mini | $0.25 | $2.00 | Mid-tier OpenAI |
| Grok 4.1 Fast | $0.20 | $0.50 | Fast reasoning |
| Llama 4 Maverick | $0.22 | $0.88 | Strong open-source |
| Codestral | $0.30 | $0.90 | Budget coding |
| o3 (post-price-cut) | $0.40 | $1.60 | Cheap reasoning |
| Mistral Large 3 | $0.50 | $1.50 | European flagship |

### Mid Tier ($1.00 - $3.00 input)
| Model | Input | Output | Best For |
|---|---|---|---|
| Claude Haiku 4.5 | $1.00 | $5.00 | Fast Anthropic tasks |
| o4-mini | $1.10 | $4.40 | Reasoning tasks |
| GPT-5 | $1.25 | $10.00 | OpenAI flagship |
| Gemini 2.5 Pro | $1.25 | $10.00 | Google flagship |
| Gemini 3 Pro Preview | $2.00 | $12.00 | Top reasoning |
| GPT-4.1 | $2.00 | $8.00 | 1M context general |
| Cohere Command A | $2.50 | $10.00 | Enterprise RAG |
| Claude Sonnet 4.5 | $3.00 | $15.00 | Best coding value |
| Grok 4 | $3.00 | $15.00 | xAI flagship |

### Premium Tier ($5.00+ input)
| Model | Input | Output | Best For |
|---|---|---|---|
| Claude Opus 4.5 | $5.00 | $25.00 | Deep reasoning |

---

## 3. Context Window Comparison

| Context Size | Models |
|---|---|
| **10M tokens** | Llama 4 Scout |
| **1M tokens** | GPT-4.1 family, Gemini 2.5/3 Pro, Gemini 2.5 Flash, Llama 4 Maverick, Claude Sonnet 4.5 (beta) |
| **400K tokens** | GPT-5/5.2 |
| **256K tokens** | Qwen3-235B, Cohere Command A |
| **200K tokens** | Claude Opus 4.5, Claude Sonnet 4.5 (default), o3, o4-mini |
| **164K tokens** | DeepSeek R1 |
| **131K tokens** | Grok 4 (2M available at higher price) |
| **128K tokens** | GPT-4o, DeepSeek V3, Mistral Large 3, most others |
| **32K tokens** | Codestral |

---

## 4. Special Capabilities Matrix

| Capability | Best Models |
|---|---|
| **Tool use / Function calling** | GPT-5, Claude Sonnet 4.5, Gemini 3 Pro, Grok 4, GPT-4.1 |
| **Vision (image understanding)** | GPT-4o, Gemini 3 Pro, Claude Sonnet 4.5, Grok 2 Vision, Llama 4 (native multimodal) |
| **Audio input** | Gemini 3 Pro (native), GPT-4o (Whisper integration) |
| **Audio output (TTS)** | OpenAI TTS, ElevenLabs, Cartesia Sonic |
| **Structured JSON output** | GPT-5, GPT-4.1, Claude Sonnet 4.5, Gemini (all support native JSON mode) |
| **Code execution** | Grok 4 (built-in sandbox), OpenAI Code Interpreter |
| **Web search (built-in)** | Grok 4 (X search + web), Gemini (Google Search grounding) |
| **Extended thinking/reasoning** | o3, o4-mini, Claude Opus 4.5, Claude Sonnet 4.5, Gemini 3 Pro, DeepSeek R1 |
| **Batch processing (50% off)** | OpenAI (all), Anthropic (all), Google (all), DeepSeek |

---

## 5. Open Source vs. Proprietary

| Type | Models |
|---|---|
| **Fully Open (MIT/Apache)** | DeepSeek V3/R1, Llama 4, Qwen3, Mistral (most models), GLM-4.7 |
| **Open Weights (restricted license)** | Some Mistral models |
| **Proprietary** | GPT-5/4.1/o3, Claude, Gemini, Grok, Cohere Command |

---

## 6. Best Model for Each Task

### Cheapest for Simple Text Summarization/Classification
**Winner: DeepSeek V3.2 Exp** ($0.021/$0.32) or **Mistral Nemo** ($0.02/$0.06)
- Runner-up: GPT-5 Nano ($0.05/$0.40), Gemini 2.0 Flash-Lite ($0.075/$0.30)
- For absolute minimum cost with acceptable quality, DeepSeek V3.2 Exp at ~2 cents per million input tokens is unbeatable. Self-hosting DeepSeek or Llama models eliminates API costs entirely.

### Best for Coding
**Winner: Claude Sonnet 4.5** ($3.00/$15.00) -- 77-82% SWE-bench Verified
- Runner-up: Gemini 3 Pro Preview (#1 on LM Arena), GPT-5.2 (74.9% SWE-bench)
- Budget option: DeepSeek V3.2 Exp (open source, strong coding) or Grok Code Fast 1 ($0.20/$0.50)
- Open-source: GLM-4.7 Thinking (89% LiveCodeBench, free to self-host)

### Best for Reasoning/Analysis
**Winner: Claude Opus 4.5** ($5.00/$25.00) -- deepest reasoning with extended thinking
- Runner-up: o3 ($0.40/$1.60 post-price-cut -- exceptional value), Gemini 3 Pro Preview
- Budget: DeepSeek R1 0528 ($0.45/$2.15) -- o1-level reasoning at ~95% lower cost
- o3 at $0.40 input is arguably the best reasoning-per-dollar in January 2026

### Best for Embeddings
**Winner: Voyage AI voyage-3.5** ($0.06/1M tokens) -- top MTEB benchmarks, 32K context
- Runner-up: OpenAI text-embedding-3-large ($0.13/1M) -- best ecosystem integration
- Budget: OpenAI text-embedding-3-small ($0.02/1M) -- cheapest quality option
- Multimodal: Cohere Embed v4 ($0.12/1M) -- text + image embeddings
- For RAG with reranking: Cohere Embed v4 + Rerank 3.5 ($2.00/1K searches)

### Best for Vision/Image Understanding
**Winner: Gemini 3 Pro Preview** -- native multimodal, 1M context, processes video natively
- Runner-up: GPT-4o, Claude Sonnet 4.5, Llama 4 Maverick (native multimodal MoE)
- Budget: Gemini 2.5 Flash ($0.15 input) with vision capabilities

### Best for Audio Transcription
**Winner: Deepgram** ($0.0043/min, 14.5% WER, real-time capable)
- Most accurate: Google Chirp 2 (11.6% WER, $0.96/hr, batch only)
- Best quality real-time: ElevenLabs Scribe v2 (150ms latency, 90+ languages)
- Cheapest: OpenAI Whisper ($0.006/min, open-source self-hostable)

### Best for Text-to-Speech
**Winner: ElevenLabs** -- best voice quality, cloning, emotional expression
- Fastest latency: Cartesia Sonic (~$0.05/1K chars)
- Cheapest: Speechmatics ($0.011/1K chars, 11-27x cheaper than ElevenLabs)
- Most expressive: Hume AI Octave (natural language emotion control)

### Best for Structured Data Extraction
**Winner: GPT-5 / GPT-4.1** -- native JSON mode, strongest schema adherence
- Runner-up: Claude Sonnet 4.5 (excellent structured output), Gemini 3 Pro
- Budget: GPT-5 Nano (92.5-99.4% accuracy with TOON format)
- All major providers now support native structured/JSON output modes

### Best for Real-Time/Low-Latency Needs
**Winner: Grok 4.1 Fast** ($0.20/$0.50) -- near-frontier quality at minimal cost and latency
- Runner-up: GPT-5 Nano ($0.05/$0.40), Gemini 2.5 Flash ($0.15/$0.60)
- For streaming: Fireworks AI hosting of Llama 4 Maverick (145 tokens/sec)

---

## 7. Cost Optimization Strategies

| Strategy | Savings | Available On |
|---|---|---|
| **Batch API** | 50% off | OpenAI, Anthropic, Google, DeepSeek |
| **Prompt caching** | Up to 90% on repeated prefixes | Anthropic (0.1x reads), Google (75% off), DeepSeek (75% off) |
| **Self-hosting open models** | 100% API savings | DeepSeek, Llama, Qwen, Mistral, GLM |
| **Context caching** | 50-75% off cached tokens | Google, Anthropic, OpenAI |
| **Output optimization** | Variable | All (keep responses concise -- output costs 3-8x input) |

---

## 8. Key Trends in January 2026

1. **Price deflation continues**: o3 dropped 80% in price; Claude Opus 4.5 is 67% cheaper than Opus 4.
2. **MoE architectures dominate**: Llama 4, Mistral Large 3, Qwen3, and DeepSeek all use mixture-of-experts for better performance per dollar.
3. **Open-source near parity**: GLM-4.7 matches GPT-5.2 on coding benchmarks; DeepSeek R1 matches o1 at 95% less cost.
4. **Context windows expanding**: 1M tokens is becoming standard; Llama 4 Scout offers 10M.
5. **Reasoning modes becoming standard**: Extended thinking/chain-of-thought is available on Claude, Gemini, OpenAI o-series, and DeepSeek R1.
6. **Chinese labs competitive**: DeepSeek, Qwen, GLM, Doubao, and Kimi are all producing frontier-quality models at dramatically lower prices.

---

## Sources

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Platform Pricing Docs](https://platform.openai.com/docs/pricing)
- [Anthropic Claude Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [Mistral AI Pricing](https://mistral.ai/pricing)
- [xAI Models and Pricing](https://docs.x.ai/docs/models)
- [Cohere Pricing](https://cohere.com/pricing)
- [Alibaba Cloud Model Studio Pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)
- [Together AI Pricing](https://www.together.ai/pricing)
- [Fireworks AI Pricing](https://fireworks.ai/pricing)
- [LLM Stats Benchmarks](https://llm-stats.com/benchmarks)
- [Best Coding LLMs January 2026 - WhatLLM](https://whatllm.org/blog/best-coding-models-january-2026)
- [Top 9 LLMs January 2026 - Shakudo](https://www.shakudo.io/blog/top-9-large-language-models)
- [Best Embedding Models - Elephas](https://elephas.app/blog/best-embedding-models)
- [Embedding Models Comparison - AIM](https://research.aimultiple.com/embedding-models/)
- [Context Window Comparison - Elvex](https://www.elvex.com/blog/context-length-comparison-ai-models-2026)
- [Price Per Token - All Providers](https://pricepertoken.com/pricing-page/provider/anthropic)
- [Anthropic Review 2026 - Hackceleration](https://hackceleration.com/anthropic-review/)
- [AI Model Pricing Comparison - Privacy AI](https://privacyai.acmeup.com/api-model-pricing.html)
- [DeepSeek V3.2 Price Cut - VentureBeat](https://venturebeat.com/ai/deepseeks-new-v3-2-exp-model-cuts-api-pricing-in-half-to-less-than-3-cents)
- [Best TTS APIs 2026 - Speechmatics](https://www.speechmatics.com/company/articles-and-news/best-tts-apis-in-2025-top-12-text-to-speech-services-for-developers)
- [Best STT APIs 2026 - AssemblyAI](https://www.assemblyai.com/blog/best-api-models-for-real-time-speech-recognition-and-transcription)
