# Chapter 9: Setup & Infrastructure — The Boring Stack That Works

> "The best infrastructure is the one you forget about because it just works."

Most AI practitioners spend 80% of their time choosing tools and 20% deploying them. Invert that ratio.

A five-person startup spent five months migrating to Kubernetes instead of shipping product. Their MVP had been running fine on Docker Compose across two VMs. But they didn't feel "serious" without Kubernetes. By the time the infrastructure was production-ready, they'd burned through runway solving problems they didn't have. Meanwhile, 73% of Kubernetes clusters run at under 25% utilization, with startups wasting $50K-$200K annually on over-provisioning.

This chapter is the antidote. The simplest infrastructure that actually works, with real costs, real failure modes, and no "it depends."

---

## 9.1 The Day 1 Setup — The Honest Minimum

Every tutorial front-loads complexity: Conda, Jupyter, twelve packages, CUDA toolkit, vector database — before the reader has made a single API call. This is backwards.

**What you actually need on day one:**

1. **Python 3.11+** — 25% speed improvement over 3.10, mature library support. 3.12/3.13 are fine but occasionally break C extension packages.
2. **One API key** — OpenAI or Anthropic. Not both. Budget $5-20 for experimentation — enough for thousands of calls with smaller models.
3. **Four packages:** `pip install openai anthropic python-dotenv requests`
4. **A text editor with a terminal** — VS Code, Cursor, or anything. The editor matters less than people think.

You don't need LangChain, LlamaIndex, ChromaDB, or any framework on day one. Frameworks are useful after you understand what they abstract away. If you start with LangChain before making a raw API call, you won't understand what breaks when it breaks — and it will break.

**Your first script should be seven lines:**

```python
from openai import OpenAI
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

### Package Management: uv

The Python packaging ecosystem has been broken for twenty years. pip has no lock files. Poetry is slow. Conda creates new problems.

**Use uv.** Written in Rust, 10-100x faster than pip. Cold-installing JupyterLab: 21 seconds with pip, 2.6 seconds with uv. But speed isn't the real reason — uv replaces multiple tools with one: Python versions, virtual environments, dependencies, and lock files in a single binary.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init my-ai-project && cd my-ai-project
uv python install 3.11
uv add openai anthropic python-dotenv
```

**Choose uv when:** Starting any new Python project. Always.

**Avoid when:** Existing Poetry project with no pain points. Migration has a cost; only pay it if you feel friction.

---

## 9.2 Security First — The Four-Minute Rule

Before anything else: **leaked credentials on GitHub are found by bots within four minutes.** Treat every accidental commit as an active breach.

### The Scale of the Problem

In 2024, GitHub detected **39 million leaked secrets** across repositories. OpenAI API keys saw a 1,212x increase in leak frequency between 2022 and 2023, making them the most commonly leaked secret type. One team committed AWS keys at 2:04 PM. Automated bots found them within minutes. By morning: 487 GPU instances for crypto mining, **$89,000 bill**. Another startup's leaked OpenAI key: 280,000 GPT-4 calls, $8,400 in 6 hours.

### The Four Ways Keys Leak

**1. Committed to Git.** The classic. You hardcode during testing, forget to remove, push to public repo. Bots scan continuously for patterns like `sk-proj-` and `sk-ant-`.

**2. Baked into Docker images.** In November 2025, researchers found over 10,000 Docker Hub images exposing secrets from 100+ companies. Root cause: `COPY . .` in Dockerfiles copies `.env` files into image layers permanently. `.gitignore` doesn't apply to Docker build context — you need a separate `.dockerignore`.

**3. Leaked by AI coding agents.** The newest vector. Security research demonstrated that Claude Code and Cursor automatically load `.env` files as context without explicit consent. Values can appear in API calls, logs, or suggestions.

**4. Logged to stdout/stderr.** Debug statement prints request headers containing `Authorization: Bearer sk-...`. That log goes to CI/CD, monitoring service, or shared terminal.

### Non-Negotiable Protections

**Before your first commit:**

```gitignore
# .gitignore — MINIMUM for any AI project
.env
.env.*
!.env.example
__pycache__/
*.pyc
.venv/
venv/
*.bin
*.pt
*.onnx
*.pkl
models/
embeddings/
```

**Before your first Docker build:** Create a `.dockerignore` with the same entries. Docker ignores `.gitignore` entirely.

**Before your first API call:** Set spending limits on every provider. OpenAI, Anthropic, and AWS all support billing alerts. Set them at 50% and 80% of your monthly budget.

**Enable GitHub push protection.** Since February 2024, GitHub blocks pushes containing known secret patterns for public repos. Enable it for private repos too.

---

## 9.3 The Hosting Decision

Most solo developers and small teams are massively over-provisioned — running $200/month AWS setups for workloads that run fine on a $5 VPS.

### The Three Tiers

**Budget VPS (Hetzner, DigitalOcean, Hostinger).** A Hetzner CX22: 2 vCPUs, 4GB RAM, 40GB NVMe for **EUR 3.79/month**. This comfortably runs: a vector database (Qdrant with 50K+ vectors), a web application, a reverse proxy with SSL, multiple Python scripts, cron jobs, and a Tor proxy — simultaneously. Not hypothetical; this is the actual Ydrasil production stack.

**Major Cloud (AWS, GCP, Azure).** AWS EC2 t3.medium (equivalent specs): ~$30/month. Add RDS ($15-50), load balancer ($16), S3, and your "simple app" costs $80-150/month. The real cost isn't compute — it's cognitive overhead: IAM policies, VPC configuration, security groups, 200+ services. A solo developer spends more time managing AWS than building features.

**Serverless (Lambda, Cloud Functions).** AWS Lambda: $0.20 per million requests. For intermittent workloads (webhook firing 100 times/day), essentially free. But: 15-minute execution limit and limited memory make it unsuitable for AI agent workflows that run for minutes, document processing, or vector database operations.

**Choose a VPS when:** You run always-on services. Your budget is under $50/month. You want full control. This covers 90% of AI practitioners.

**Avoid a VPS when:** You need auto-scaling for unpredictable spikes, or compliance requiring managed services with SLAs.

**Choose serverless when:** Genuinely intermittent workloads — webhooks, scheduled batch jobs, event-driven pipelines.

**Avoid serverless when:** Long-running processes, persistent connections, or local state. AI agents that run for minutes are a bad fit.

### Failure Modes

- **The AWS trap:** Starting with AWS "because that's what companies use." Three months later: $120/month for what runs on a $5 VPS, plus 40 hours learning IAM instead of building product.
- **The Hetzner trap:** Cheapest VPS, no backups. Disk fails. Everything gone. Budget hosting is fine. Budget hosting without backup is gambling.

---

## 9.4 What to Self-Host (and What Not To)

### Self-Host These

**Vector databases.** Qdrant runs in one Docker container, ~200MB RAM for 50K vectors, zero maintenance. Pinecone's managed equivalent: $108/month. Self-hosted Qdrant on a $5 VPS: $5/month total. **20x cost difference.** Under 1M vectors, there's no reason for managed.

**Web apps.** Nginx or Node behind a reverse proxy, trivial with Docker. Vercel/Netlify charge premium the moment you need server-side logic.

**Automation.** n8n self-hosted: free, unlimited executions. n8n cloud: $24/month for 2,500 executions. Self-hosting saves $300-800/year once you're running 50+ automations daily.

**Cron jobs.** Systemd timers and cron are free, reliable, simple. Managed alternatives add cost and complexity for zero benefit at small scale.

### Don't Self-Host These

**LLM inference** (without GPUs). A 7B model on VPS CPU: 2-3 tokens/second — unusable. GPU instances cost $1-3/hour. API equivalent for a solo practitioner: $5-30/month.

**Email delivery.** Deliverability requires IP reputation, DKIM/SPF/DMARC, constant monitoring. Use SendGrid (100 free/day). Debugging self-hosted email exceeds subscription cost within the first week.

**DNS.** Cloudflare: free DNS + DDoS protection + CDN. Self-hosted DNS is a security liability with no upside.

---

## 9.5 The Production Stack

### Reverse Proxy & SSL

Every exposed AI service needs a reverse proxy with SSL. Without SSL, API keys transit in plaintext.

**Use Caddy.** Automatic HTTPS out of the box. Complete production config:

```
app.example.com {
    reverse_proxy localhost:3000
}
api.example.com {
    reverse_proxy localhost:8080
}
```

Two domains, reverse proxied, automatic SSL. Compare to 40+ lines for equivalent Nginx config. Caddy obtains, provisions, and renews Let's Encrypt certificates automatically.

**AI-specific concerns:** Set proxy timeouts to 300+ seconds (AI requests are long). Increase body limits to 10-50MB for document uploads. Add rate limiting — one bad actor can run up $500 in API costs through your proxy.

### Monitoring — The Minimum That Works

**Layer 1:** UptimeRobot (free, 50 monitors). Every public endpoint. Catches "server is down" and "SSL expired."

**Layer 2:** Systemd `Restart=on-failure` for services. Cron output to log files with a checker that alerts if jobs haven't run.

**Layer 3:** Weekly API cost review. Check Anthropic and OpenAI dashboards every Sunday. Five minutes that prevents $200 surprises.

**Layer 4:** Custom `/health` endpoints that check actual dependencies:

```json
{"status": "ok", "qdrant": "connected", "vectors": 50142, "disk_free_gb": 24.3}
```

**Avoid Grafana/Prometheus** unless you have 50+ services or enjoy infrastructure work. For a solo dev, the maintenance time exceeds the debugging time it saves.

### Backup — The "My VPS Dies" Plan

**What to back up:**

| Priority | What | Why |
|----------|------|-----|
| Critical | Config files, .env, credentials | Lose this, locked out of everything |
| Critical | Git repo (pushed to remote) | IS your backup |
| Critical | Vector DB snapshots | Re-embedding costs $10-50+ and hours |
| Important | Raw data before embedding | Without this, snapshots are unrecoverable |
| Nice to have | Logs, session history | Inconvenient to lose, not fatal |

**Daily automated backup:** Cron at 04:00 — Qdrant snapshot, tar configs + data, push to offsite (Backblaze B2: $0.005/GB/month). A 5GB AI stack backup costs $0.025/month. No excuse for not having offsite backups.

**Recovery should take under 2 hours:** New VPS (5 min) → clone repo (2 min) → Docker Compose up (15 min) → restore Qdrant snapshot (10-30 min) → update DNS (5 min) → restore .env (5 min) → verify health (10 min).

**Failure mode:** Backups on the same disk as the server. Disk fails, lose both. Always offsite.

---

## 9.6 The Simplicity Principle

The boring infrastructure that works isn't exciting enough for conference talks. That's exactly why it works.

### VPS + Docker Compose > Kubernetes

A $20/month VPS with Docker Compose: one machine to SSH into, `docker compose up -d` deployment, predictable cost, full data control, no IAM policies. Same on AWS: EC2, RDS, ECR, ALB, IAM, VPC, Security Groups, CloudWatch, plus a bill requiring a spreadsheet.

**Upgrade when:** 10+ services, multiple teams deploying independently, genuine auto-scaling need, dedicated platform engineer.

### cron + systemd > Airflow

Airflow requires Postgres, web server, scheduler, workers. A distributed system. For running a script every hour:

```
0 * * * * /usr/bin/python3 /opt/scripts/fetch.py >> /var/log/fetch.log 2>&1
```

**Upgrade when:** 20+ scheduled jobs with complex dependencies, multiple teams need visibility.

### SQLite > Postgres (for most AI projects)

No server process, no config, no user management. Single file. Back it up with `cp`. Faster for read-heavy workloads (no network round-trip).

**Upgrade when:** Concurrent writes from multiple processes, full-text search at scale, data exceeds single disk.

### The Pattern

Every "upgrade" above follows the same logic: **the simple version handles 95% of cases. The complex version exists for the 5%. Don't pay the 5% tax until you're in the 5%.**

---

## 9.7 Cost Management

AI infrastructure costs spiral in ways traditional infrastructure doesn't. A web server serves pages at constant cost. An AI service's cost varies with usage, model choice, and bugs.

### Where AI Costs Hide

- **Embedding 50K documents** (avg 500 tokens): 25M tokens = $0.50
- **100 RAG queries/day** with Sonnet: ~$49.50/month
- **One runaway agent loop** (500 requests before notice): $25-75 in a single incident
- **The staging environment nobody uses** making real API calls for 3 months: $200 in waste

### Controls That Work

1. **Hard spending limits** — set on every provider, day one, not "when we go to production"
2. **`max_tokens` on every API call** — never rely on the model to stop generating
3. **Circuit breakers** — if error rate >20% over 5 minutes, stop calling, alert a human
4. **Model routing** — Haiku for simple lookups, Sonnet for standard tasks, Opus for complex reasoning. Reduces costs 40-60%.
5. **Separate API keys per environment** — dev experiments can't consume production budget

---

## 9.8 Hype vs. Reality Scorecard

| Tool | Hype | Reality | Verdict |
|------|------|---------|---------|
| **Kubernetes** | 9 | 3 (for most) | Skip until 10+ services + platform engineer. Docker Compose handles 95% of cases. |
| **Terraform** | 7 | 4 (for solo) | Overkill for single VPS. A documented checklist + docker-compose.yml is your IaC. |
| **Airflow** | 7 | 3 (for small) | A distributed system for running scripts. cron + systemd until 20+ jobs. |
| **Docker** | 8 | 8 | Rare honest match. 30 min Dockerfile tax, years of environment reproducibility payoff. |
| **GitHub Actions** | 7 | 7 | Genuinely useful. Simple YAML, free for public repos. One of the few that delivers. |
| **Managed Vector DBs** | 7 | 4 | Self-hosted Qdrant at 1/20th the cost until you need multi-region SLAs. |
| **MLOps Platforms** | 6 | 3 | Overkill if calling APIs, not training models. Adopt only for fine-tuning/custom training. |
| **Caddy** | 5 | 8 | Under-hyped. Automatic SSL in 3 lines. Should be default for all new projects. |

**Pattern:** Infrastructure tools built for teams of 50 get adopted by teams of 1. The complexity tax is real. The value only appears at scale.

---

## 9.9 Our Setup

The Ydrasil production stack, running since late 2025:

- **Hosting:** Hostinger VPS (Ubuntu, single machine, ~$5/month)
- **Reverse proxy:** Nginx with Let's Encrypt (would choose Caddy if starting today)
- **Services:** Docker containers — webapp, Qdrant, Python scripts
- **Scheduling:** cron for daily backups, embedding jobs, monitoring
- **Process management:** systemd for long-running services
- **Backup:** Daily cron at 04:00 → Qdrant snapshot + config tar → offsite. Plus Hostinger VPS snapshots.
- **Monitoring:** UptimeRobot (free) + systemd restart-on-failure + weekly API cost review
- **Secrets:** `.env` files, `.gitignore`'d, spending limits on all API providers
- **Version control:** Git → GitHub. Everything committed except .env, models, and data.

**Total infrastructure cost:** ~$5-10/month (VPS + domain). API costs separate ($30-50/month).

**What we'd change:** Caddy instead of Nginx (simpler SSL). More aggressive offsite backup testing. Otherwise — the boring stack works. It's been running for months with near-zero maintenance. That's the point.

---

## The Infrastructure Decision Tree

```
START: "I need to deploy an AI project"
│
├─ Day 1 (just starting)
│   └─ Python 3.11 + uv + one API key + .env + .gitignore
│       └─ STOP. Build something. Add infrastructure when walls appear.
│
├─ Ready to deploy
│   ├─ How many users?
│   │   ├─ Just me → Single VPS ($5-20/month) + Docker Compose
│   │   ├─ <1,000 → Same VPS + Caddy SSL + UptimeRobot
│   │   └─ >1,000 → Now consider cloud provider or managed services
│   │
│   ├─ Need a database?
│   │   ├─ Vector search → Self-hosted Qdrant (Docker)
│   │   ├─ Relational, single user → SQLite
│   │   └─ Relational, concurrent → Postgres (still self-hosted on VPS)
│   │
│   └─ Scheduling needed?
│       ├─ <10 jobs → cron + systemd
│       └─ >20 jobs, multiple teams → Now consider Airflow
│
├─ Security checklist (non-negotiable)
│   ├─ .gitignore + .dockerignore configured ✓
│   ├─ Spending limits on all API providers ✓
│   ├─ No secrets in code, images, or logs ✓
│   ├─ Firewall: allow only 22, 80, 443 ✓
│   └─ Services bound to localhost unless explicitly public ✓
│
└─ Backup (non-negotiable)
    ├─ Code in Git, pushed to remote ✓
    ├─ Daily automated Qdrant snapshots → offsite ✓
    ├─ .env backup (encrypted, separate location) ✓
    └─ Recovery plan written and tested ✓
```

---

*The infrastructure that matters most is not the infrastructure — it's the AI workflows running on top of it. Get the foundation right, make it boring, then forget about it and build. Every hour spent optimizing infrastructure for hypothetical scale is an hour not spent on the product that determines whether you need scale at all.*

**Key sources:** GitHub Blog (39M leaked secrets, 2024) · GitGuardian State of Secrets Sprawl 2024/2025 · OWASP LLM Top 10 2025 · Legit Security GenAI Exposure Research · Hetzner/DigitalOcean/AWS Pricing (2026) · Real Python uv Guide · Docker Hub Secrets Leak (The Register, 2025) · Kubernetes Cost Analysis (DEV Community)
