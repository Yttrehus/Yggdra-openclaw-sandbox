# Chapter 9 Research: Setup & Infrastructure -- From Zero to Production

**Purpose:** Practitioner-focused guide to development environment setup for AI projects. Not Docker 101. Not "install Python." The decisions that actually matter and the failures that actually happen.
**Date:** 2026-02-09
**Target:** ~2500 words of usable material

---

## 1. The "Day 1" Setup -- The Honest Minimum

### What You Actually Need

Every AI tutorial starts with fifteen minutes of setup instructions you skip. Here is what you genuinely need on day one, and nothing more:

**Python 3.11+.** Not 3.8, not 3.13. Python 3.11 gave a 25% speed improvement over 3.10 and has mature library support. Python 3.12 and 3.13 are fine but occasionally break packages that rely on C extensions. If something fails to install, try 3.11 first.

**An API key for one model provider.** Start with OpenAI or Anthropic. Not both. You do not need access to five providers on day one. You need one working API call. OpenAI's API starts at pay-as-you-go with no minimum; Anthropic is similar. Budget $5-20 for experimentation. That is enough for thousands of API calls with smaller models.

**Four Python packages:**
```
pip install openai anthropic python-dotenv requests
```

That is it. You do not need LangChain, LlamaIndex, ChromaDB, or any framework on day one. Frameworks are useful after you understand what they abstract away. If you start with LangChain before you have made a raw API call, you will not understand what breaks when it breaks -- and it will break.

**A text editor with a terminal.** VS Code, Cursor, or even Sublime Text. The editor matters less than people think. What matters is that you can run Python and see output without switching windows.

### The First Script That Matters

Your first AI script should be seven lines:

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print(response.choices[0].message.content)
```

If this runs, you have a working AI development environment. Everything else is optimization.

**Choose this approach when:** You are starting from zero, or you want to teach someone else the fundamentals.

**Avoid when:** You already have a working environment and just need to add a new capability.

### What Most Tutorials Get Wrong

Most tutorials front-load complexity. They install Conda, create a Jupyter environment, install twelve packages, configure a CUDA toolkit, and set up a vector database before the reader has made a single API call. This is backwards. The practitioner's approach: make one thing work, then add complexity when you need it. The Ladder of AI Solutions applies to infrastructure too -- start from the simplest rung.

---

## 2. Local Development Environment -- What Tutorials Skip

### Editor Choice: VS Code vs. Cursor

**Our recommendation: Cursor.** Since Cursor is a VS Code fork, you get everything VS Code offers -- extensions, themes, keybindings, terminal integration -- plus native AI features that VS Code bolts on through extensions. Cursor indexes your entire codebase for context-aware completions and can edit multiple files simultaneously through its Composer feature. As of early 2026, Cursor has become the default editor for AI-heavy development work ([Monday.com, 2026](https://monday.com/blog/rnd/cursor-ai-integration/); [DigitalOcean, 2026](https://www.digitalocean.com/resources/articles/github-copilot-vs-cursor)).

The migration cost is zero. Import your VS Code settings, extensions, and keybindings in one click. If Cursor disappears tomorrow, you move back to VS Code with no friction. This is a two-way door -- try it, and reverse if you dislike it.

**Choose Cursor when:** You write code daily and want AI-assisted editing without managing multiple extensions.

**Avoid when:** You work in a corporate environment that restricts editor choices, or you need VS Code's Remote SSH/container features which can behave differently in Cursor.

### Package Management: uv, and Why

The Python packaging ecosystem has been a mess for twenty years. pip works but has no lock files, no environment management, and slow dependency resolution. Poetry added structure but imposed its own conventions and is slow. Conda solves some problems but creates others (mixing conda and pip is a reliable source of environment corruption).

**Our recommendation: uv.** Written in Rust by the team behind Ruff (the fast Python linter), uv is 10-100x faster than pip. Cold-installing JupyterLab takes 21 seconds with pip and 2.6 seconds with uv. But speed is not the real reason to use it ([Real Python, 2025](https://realpython.com/uv-vs-pip/); [DataCamp, 2025](https://www.datacamp.com/tutorial/python-uv)).

The real reason: uv replaces multiple tools with one. It manages Python versions, virtual environments, dependencies, and lock files. It is compatible with existing `requirements.txt` files, so you do not need to rewrite your project structure. And it is a single binary -- no bootstrapping problems.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project with Python 3.11 and virtual environment
uv init my-ai-project
cd my-ai-project
uv python install 3.11
uv venv --python 3.11

# Add dependencies (generates lock file automatically)
uv add openai anthropic python-dotenv
```

uv uses the PubGrub algorithm for dependency resolution, borrowed from Dart's package manager. When it hits a conflict, it applies conflict-driven clause learning from SAT solvers to skip dead ends -- making it dramatically faster on complex dependency graphs ([Nesbitt, 2025](https://nesbitt.io/2025/12/26/how-uv-got-so-fast.html)).

**Choose uv when:** Starting any new Python project. Always.

**Avoid when:** You have an existing Poetry project with complex pyproject.toml configurations and no pain points. Migration has a cost; only pay it if you are feeling friction.

### .env Files: The Simplest Secrets Management

Every project needs a `.env` file. Every `.gitignore` needs to exclude it. This is not optional.

```
# .env (NEVER commit this)
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

```python
# Load in your code
from dotenv import load_dotenv
load_dotenv()
# Keys are now in os.environ
```

The pattern is simple. The failure mode is also simple: you commit the `.env` file. We cover this in detail in Section 3.

---

## 3. API Key Management & Security -- How Keys Leak and What It Costs

### The Scale of the Problem

In 2024, GitHub detected **39 million leaked secrets** across its repositories -- API keys, tokens, credentials, connection strings. Not 39 thousand. 39 million ([GitHub Blog, 2025](https://github.blog/security/application-security/next-evolution-github-advanced-security/)). A separate analysis found 13 million API credentials sitting in public repositories alone ([Medium/InstaTunnel, 2025](https://medium.com/@instatunnel/github-secret-leaks-the-13-million-api-credentials-sitting-in-public-repos-1a3babfb68b1)).

The average cost of a breach involving compromised credentials: **$4.88 million** per incident according to the IBM Cost of Data Breach Report 2024 -- a 10% increase from the previous year. For individual developers, the numbers are smaller but still painful: leaked AWS keys have resulted in charges exceeding $50,000 before detection when attackers spin up crypto miners ([BleepingComputer, 2025](https://www.bleepingcomputer.com/news/security/github-expands-security-tools-after-39-million-secrets-leaked-in-2024/)).

### The Four Ways Keys Leak

**1. Committed to Git.** The classic. You hardcode an API key during testing, forget to remove it, and push to a public repo. Bots scan GitHub continuously for patterns like `sk-proj-` and `sk-ant-`. Your key is compromised within minutes -- sometimes seconds.

**2. Baked into Docker images.** In November 2025, researchers found **over 10,000 public Docker Hub images** exposing secrets from more than 100 companies. 42% of exposed images contained five or more secrets each. The root cause: `.env` files copied into images during `docker build`. A `COPY . .` instruction does not care about your `.gitignore` -- it copies everything in the build context ([The Register, 2025](https://www.theregister.com/2025/12/11/docker_hub_secrets_leak/); [CyberPress, 2025](https://cyberpress.org/docker-hub-images-found-leaking/)).

One documented case: a team's Docker image containing a `.env` file was publicly accessible on Docker Hub. Someone found it, extracted the AWS credentials, and ran crypto miners. The AWS bill spiked to $4,700 when it should have been $800.

**3. Leaked by AI coding agents.** This is the newest vector. Knostic's security research in 2025-2026 demonstrated that coding agents like Claude Code and Cursor automatically load `.env` files from project directories without explicit user consent. The agent reads your secrets as context, and those values can appear in API calls, logs, or suggestions. One Knostic customer found their Cursor agent attempting to upload a local file containing an API key to the cloud ([Knostic, 2025](https://www.knostic.ai/blog/claude-cursor-env-file-secret-leakage); [The Register, 2026](https://www.theregister.com/2026/01/28/claude_code_ai_secrets_files/)).

**4. Logged to stdout/stderr.** You print a debug statement that includes the request headers. The headers contain your `Authorization: Bearer sk-...` token. That log goes to a monitoring service, a CI/CD artifact, or a shared terminal session.

### How to Prevent It

**Non-negotiable `.gitignore` entries for every AI project:**

```gitignore
# Secrets
.env
.env.*
!.env.example

# Python
__pycache__/
*.pyc
.venv/
venv/

# Models and data (covered in Section 5)
*.bin
*.pt
*.onnx
*.pkl
embeddings/
models/

# IDE
.vscode/
.cursor/
```

**Use `.dockerignore` -- it is not the same as `.gitignore`.** Docker's build context ignores `.gitignore` entirely. You need a separate `.dockerignore` file:

```dockerignore
.env
.env.*
.git
__pycache__
*.pyc
```

**Enable GitHub push protection.** Since February 2024, GitHub scans public repo pushes for known secret patterns and blocks them before they reach the remote. This is on by default for public repos but opt-in for private repos. Enable it. It has prevented millions of leaks ([GitHub Blog, 2025](https://github.blog/security/application-security/next-evolution-github-advanced-security/)).

**Set spending limits on API providers.** OpenAI, Anthropic, and AWS all support billing alerts and hard spending caps. Set them before you write your first line of code, not after you get a surprising bill.

**For AI coding agents:** Create a `.claudeignore` or equivalent deny file that excludes `.env` from the agent's file access. Be aware this is an evolving area -- the protections are imperfect ([GitHub Issue #9637](https://github.com/anthropics/claude-code/issues/9637)).

**Choose environment variables when:** Your project has fewer than ten secrets and runs on one or two machines.

**Avoid environment variables when:** You manage secrets across multiple services, environments (dev/staging/prod), or team members. At that point, use a secrets manager -- AWS Secrets Manager, HashiCorp Vault, or even `doppler`. The `.env` file is a starting point, not a destination.

---

## 4. Docker for AI Practitioners -- When It Helps vs. When It Is Overhead

### The Honest Assessment

Docker adds near-zero performance overhead, even for GPU workloads. That is not the issue. The issue is cognitive overhead: Dockerfiles, build contexts, networking, volumes, multi-stage builds. For a solo practitioner running Python scripts against an API, Docker is overhead you do not need.

**Choose Docker when:**
- You are deploying an API service that others will call (FastAPI + model inference)
- You need reproducible environments across team members or CI/CD
- You are running multi-service stacks (app + vector database + embedding service)
- You need GPU isolation for multiple models on the same machine

**Avoid Docker when:**
- You are prototyping with API calls to hosted models (OpenAI, Anthropic)
- You are the only person running the code
- You are experimenting and changing dependencies frequently (rebuilding images gets tedious fast)

### Practical Patterns

**Pattern 1: API service with docker-compose.** The most common AI Docker pattern is a FastAPI service that calls a model, paired with a vector database:

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env  # Loaded at runtime, NOT baked into image
    depends_on:
      - qdrant

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

Note: `env_file` in docker-compose loads variables at *runtime*, not build time. This is safe. `COPY .env .` in a Dockerfile bakes them into the image layer permanently. This is how the 10,000 Docker Hub leaks happened.

**Pattern 2: GPU passthrough for local models.** Docker's NVIDIA Container Toolkit makes GPU access straightforward on Linux. As of 2025, Docker Model Runner also supports Vulkan for AMD and Intel GPUs ([Docker Blog, 2025](https://www.docker.com/blog/docker-model-runner-vulkan-gpu-support/)):

```yaml
services:
  ollama:
    image: ollama/ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
```

**Failure mode:** Forgetting to install `nvidia-container-toolkit` on the host. Docker does not give you a clear error -- it silently falls back to CPU, and you wonder why inference takes ten minutes instead of ten seconds. Always verify GPU access: `docker run --gpus all nvidia/cuda:12.0-base nvidia-smi`.

**Pattern 3: Keep model storage on a volume, not in the image.** Model weights are large (700MB to 70GB+). Baking them into a Docker image means every rebuild redownloads them, every push uploads them, and your image registry bill grows. Mount them as volumes instead. Store on fast storage (NVMe/SSD) -- model loading is I/O bound, and a spinning disk will bottleneck even a powerful GPU ([Docker Docs, 2025](https://docs.docker.com/desktop/features/gpu/)).

---

## 5. Version Control for AI Projects -- What to Commit, What Not to Commit

### The Rule

If it is generated, large, or secret, do not commit it. Everything else goes in Git.

**Commit:**
- Source code (obviously)
- Configuration files (`pyproject.toml`, `docker-compose.yml`, `Dockerfile`)
- `.env.example` (template with placeholder values, never real keys)
- `.gitignore` and `.dockerignore`
- Requirements/lock files (`requirements.txt`, `uv.lock`)
- Small reference data (< 10MB CSV files, JSON configs)
- Documentation and READMEs
- Prompts and prompt templates (these are your intellectual property)

**Never commit:**
- `.env` files with real credentials
- Model weights (`.bin`, `.pt`, `.onnx`, `.safetensors`, `.gguf`)
- Embedding databases (ChromaDB directories, Qdrant snapshots)
- Large datasets (anything over 50MB)
- Virtual environments (`venv/`, `.venv/`)
- `__pycache__/` directories
- Jupyter notebook outputs containing API responses (they may contain sensitive data or PII)

### Git LFS: Usually the Wrong Answer

Git Large File Storage (LFS) replaces large files in your repo with pointers and stores the actual files on a separate server. In theory, this solves the "large model file" problem. In practice, it creates new problems.

Git LFS costs money at scale (GitHub charges for bandwidth and storage beyond 1GB), adds complexity to clone/pull operations, and does not solve the fundamental issue: model weights change rarely and do not benefit from version control's line-by-line diffing. You are using a text versioning tool to track binary blobs.

**The better approach for models:** Do not version them in Git at all. Store models in cloud storage (S3, GCS, Azure Blob) or a model registry (HuggingFace Hub, MLflow). Reference them by name and version in your code. Download them at runtime or build time. This is what DVC (Data Version Control) formalizes -- lightweight metadata files in Git point to actual data stored externally ([Medium/Neel Shah, 2025](https://medium.com/@neeldevenshah/why-git-lfs-is-not-good-practice-for-ai-model-weights-and-why-you-should-use-dvc-instead-demo-with-3903a7ae68f5)).

**Choose Git LFS when:** You have a small number of binary files (< 1GB total) that change rarely and you want the simplicity of `git pull` fetching everything. Documentation images, small test fixtures, reference PDFs.

**Avoid Git LFS when:** You are storing model weights, large datasets, or embeddings. Use DVC, cloud storage, or a model registry instead.

### The Complete .gitignore for AI Projects

```gitignore
# === Secrets ===
.env
.env.*
!.env.example
*.pem
*.key
credentials.json

# === Python ===
__pycache__/
*.py[cod]
*.so
.venv/
venv/
*.egg-info/
dist/
build/

# === Models & Data ===
*.bin
*.pt
*.pth
*.onnx
*.safetensors
*.gguf
*.pkl
*.h5
models/
embeddings/
*.parquet
*.feather

# === Vector DBs ===
chroma_data/
qdrant_storage/
*.index

# === Notebooks ===
.ipynb_checkpoints/

# === IDE ===
.vscode/
.cursor/
.idea/

# === OS ===
.DS_Store
Thumbs.db

# === Docker ===
docker-compose.override.yml
```

### Prompt Templates: The Exception That Matters

Your prompts and prompt templates *should* be version controlled. They are source code -- they define the behavior of your system. When a prompt change causes a regression, you want `git blame` to tell you what changed and when. Store them as separate files (`prompts/summarize.txt`, `prompts/classify.json`) rather than inline strings in Python. This makes them diffable, reviewable, and testable.

**Failure mode:** Keeping prompts as inline strings across twenty Python files. When output quality drops, you have no idea which prompt changed, when, or why. Treat prompts like configuration -- externalize and version them.

---

## Summary: Day 1 Checklist

1. Install Python 3.11+ (via `uv python install 3.11`)
2. Install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
3. Get one API key (OpenAI or Anthropic)
4. Create `.env` file with the key, `.env.example` without it
5. Add `.gitignore` from the template above before your first commit
6. Set a spending limit on your API provider
7. Make one successful API call
8. Everything else can wait

The infrastructure decisions that look important on day one (Docker vs. bare metal, Poetry vs. uv, which vector database) are all two-way doors. You can change them later with minimal cost. The one-way door is committing secrets to a public repository. Get that right first. Everything else is reversible.
