# Chapter 9 Research: Infrastructure Anti-Patterns, Security Failures & The Simplicity Principle

**Research focus:** What goes wrong when AI practitioners build infrastructure. Failures, cost explosions, security disasters, and the case for boring technology.

---

## 1. The Over-Engineering Trap

The most expensive infrastructure mistake in AI is not choosing the wrong tool. It is choosing the right tool for a scale you will never reach.

### Kubernetes Before Customers

A five-person startup building a B2B SaaS product had a working MVP running on Docker Compose across a couple of VMs. It worked fine. But they did not feel "serious" without Kubernetes in production. They budgeted two weeks to learn Kubernetes and migrate workloads. It took five months. By the time the infrastructure was "production-ready," the company had burned through runway solving problems they did not have ([Medium: Kubernetes Killed My Startup](https://techpreneurr.medium.com/kubernetes-killed-my-startup-the-hidden-costs-of-cloud-native-ae9ff3664089)).

This is not an isolated story. Average startups waste $50,000-$200,000 annually on EKS overprovisioning, with 73% of Kubernetes clusters running at less than 25% utilization ([DEV Community: Kubernetes Cost Nightmares](https://dev.to/costqai/kubernetes-cost-nightmares-why-most-startups-overpay-on-eks-and-how-to-fix-it-2dg)). The cost is not just compute. It is developer time diverted from building product to managing infrastructure.

The pattern repeats with AI-specific tooling. Teams adopt LangChain, vector databases, orchestration frameworks, and managed AI platforms before writing their first working prompt. They build RAG pipelines before confirming the base model cannot answer the question. They set up MLOps monitoring before deploying a single model. Every layer adds complexity, debugging surface, and maintenance burden.

### The Infrastructure Resume Problem

Engineers often choose infrastructure to build their resume, not to solve business problems. Kubernetes on a CV looks better than "cron job on a VPS." Terraform looks better than a bash script. But the bash script ships today and the Terraform module ships next quarter.

**Choose Kubernetes when:** You have 10+ services, multiple teams deploying independently, genuine need for auto-scaling, and a dedicated platform team.

**Avoid Kubernetes when:** You have fewer than 5 services, a team under 10 engineers, predictable traffic, or you are pre-product-market-fit. Docker Compose on a single VPS handles this. Move to Kubernetes when the pain of not having it is real, not theoretical.

---

## 2. Security Disasters in AI Infrastructure

AI infrastructure has created entirely new categories of security failures. Traditional security knowledge does not cover API key economics, prompt injection, or vector database exposure.

### API Key Leaks: The $89K Lesson

GitGuardian's 2025 State of Secrets Sprawl report found 23.8 million secrets leaked on public GitHub repositories in 2024 alone, a 25% year-over-year increase. Worse: 70% of secrets leaked in 2022 remain active today ([GitGuardian: State of Secrets Sprawl 2025](https://www.gitguardian.com/state-of-secrets-sprawl-report-2025)).

OpenAI API keys saw a 1,212x increase in leak frequency between 2022 and 2023, making them the most commonly leaked secret type ([GitGuardian: State of Secrets Sprawl 2024](https://www.gitguardian.com/state-of-secrets-sprawl-report-2024)).

One documented case: a team committed AWS API keys to GitHub at 2:04 PM. Automated bots found the keys within four minutes. By morning, attackers had spun up 487 GPU instances for crypto mining, generating an $89,000 bill. The IAM user had AdministratorAccess. No CloudWatch alarms were configured. AWS credited most of the bill, but the organization still paid $7,000 ([Medium: We Got a $89K AWS Bill Overnight](https://medium.com/lets-code-future/we-got-a-89k-aws-bill-overnight-heres-what-went-wrong-b5dfd51c9a7e)).

For OpenAI keys, one startup's leaked production key resulted in 280,000 GPT-4 API calls and an $8,400 bill within 6 hours ([SANS ISC: What happens when you leak your AWS keys](https://isc.sans.edu/diary/30730)).

**The fix is not complicated.** Use `.env` files excluded via `.gitignore`. Use secret managers (even simple ones like `doppler` or `1password cli`). Set billing alerts at 50%, 80%, and 100% of your monthly budget. Rotate keys quarterly. After a leak, assume compromise within minutes, not hours.

### Prompt Injection in Production

OWASP ranks prompt injection as the #1 vulnerability in LLM applications, found in over 73% of production AI deployments during security audits ([OWASP: LLM Top 10 2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)).

Real incidents from 2024:
- **ChatGPT memory exploit:** A persistent prompt injection manipulated ChatGPT's memory feature, enabling long-term data exfiltration across multiple conversations.
- **Resume-based injection:** A job seeker hid fake skills in light gray text on a resume. The AI screening system read the hidden text and gave the candidate a higher profile score.
- **Vanna AI database tool:** A vulnerability allowed attackers to embed harmful commands into prompts, generating unauthorized SQL queries and achieving remote code execution ([NSFOCUS: Prompt Injection Analysis](https://nsfocusglobal.com/prompt-word-injection-an-analysis-of-recent-llm-security-incidents/)).
- **The Guardian test (late 2024):** Researchers created webpages with hidden prompt injection sections. When ChatGPT's browsing feature was asked to summarize those pages, the hidden prompts successfully altered the summary output.

### Open Vector Databases

Researchers scanning for publicly exposed GenAI services found alarming results. Of 959 Flowise servers discovered, 438 (45%) were vulnerable to a trivial authentication bypass (CVE-2024-31621) that exploited case-sensitivity in API endpoints (`/API/v1` vs. `/api/v1`). Researchers extracted GitHub tokens, OpenAI API keys, and hardcoded Pinecone credentials from vulnerable instances ([Legit Security: Risks in Publicly Exposed GenAI Services](https://www.legitsecurity.com/blog/the-risks-lurking-in-publicly-exposed-genai-development-services)).

Qdrant databases were found exposed on the open internet containing customer personal details and purchase information. By default, Qdrant Docker images ship without authentication enabled ([IronCore Labs: Qdrant Security](https://ironcorelabs.com/vectordbs/qdrant-security/)).

**Choose when to expose services publicly:** Never, if you can avoid it. Use private networks, VPN, or SSH tunnels. If you must expose a port, add API key authentication at minimum.

**Avoid:** Running any database — vector or otherwise — on a public port without authentication. The default for Qdrant, Redis, and many other tools is no auth. Change it before your first deployment, not after your first breach.

---

## 3. The "Works on My Machine" Problem

Python is the lingua franca of AI. Python dependency management is also one of the worst in any mainstream language.

### The Dependency Hell Cycle

A typical AI project depends on PyTorch, transformers, numpy, scipy, and dozens of transitive dependencies. Each of these has version constraints. When they conflict, you get errors like `gevent==21.8.0 requires greenlet<2.0, but sqlalchemy requires greenlet>=2.0` — a real conflict documented in the Apache Superset project ([GitHub: Superset Issue #26396](https://github.com/apache/superset/issues/26396)).

The failure mode is predictable: a developer installs packages one-by-one on their machine over weeks, each install subtly changing the dependency tree. They never record the exact versions. When deploying to production, `pip install -r requirements.txt` resolves to different versions, and the application crashes on startup.

### What Docker Solves (and Doesn't)

Docker solves environment reproducibility. Your Dockerfile pins the Python version, system packages, and application dependencies. If it works in the container locally, it works in the container in production. That alone eliminates 80% of deployment failures.

What Docker does not solve:
- **GPU driver mismatches.** Your local NVIDIA driver may differ from production. CUDA version mismatches cause silent failures or cryptic errors.
- **Data path assumptions.** Hardcoded paths to `/home/username/data/` do not exist in a container.
- **Network assumptions.** `localhost:5432` in development is `postgres:5432` in Docker Compose. Service discovery changes between environments.
- **Secret management.** Baking secrets into Docker images is worse than `.env` files — images persist in registries.

**Choose Docker when:** You are deploying anything beyond a single script. The overhead of writing a Dockerfile is 30 minutes. The time saved debugging environment issues is hundreds of hours over a project's lifetime.

**Avoid Docker when:** You are running a one-off data analysis script that will never leave your machine. But even then, consider it.

### The Minimum Viable Setup

```
project/
  Dockerfile
  docker-compose.yml
  .env              # never committed
  .env.example      # committed, documents required vars
  requirements.txt  # pinned versions (pip freeze > requirements.txt)
```

Pin everything. Not `openai>=1.0`, but `openai==1.68.2`. Use `pip freeze > requirements.txt` after confirming your environment works. Future you will be grateful.

---

## 4. Cost Explosion Stories

AI API costs are fundamentally different from traditional infrastructure costs. Traditional APIs have predictable per-request costs. LLM APIs have variable costs per request because token counts are non-deterministic. A prompt that costs $0.02 today might cost $0.15 tomorrow if the model generates a longer response.

### The Runaway Loop

The most common cost explosion: an AI agent in a retry loop. The agent calls GPT-4, gets an error, retries, gets another error, retries again — 10,000 times before anyone notices. Without rate limits or circuit breakers, this can happen over a weekend when nobody is watching.

Teams combining 50%, 80%, and 100% budget alerts with 3x rate-of-change anomaly detectors routinely catch misconfigured loops within hours. Teams without these safeguards discover the problem on their next invoice ([Lunar.dev: Unseen Challenges of AI Deployment](https://www.lunar.dev/post/beyond-the-hype-the-unseen-challenges-of-ai-deployment-and-api-management)).

### Prevention Checklist

1. **Hard spending limits.** OpenAI, Anthropic, and Google all support monthly spending caps. Set them on day one. Not "when we get to production." Day one.
2. **Per-request token limits.** Set `max_tokens` in every API call. Never rely on the model to stop generating.
3. **Circuit breakers.** If error rate exceeds 20% over 5 minutes, stop calling the API. Alert a human.
4. **Rate limiting per user.** If your application lets users trigger API calls, rate-limit per user. One abusive user should not drain your entire budget.
5. **Daily cost monitoring.** A simple script that checks your API dashboard and sends a Slack/Telegram alert if daily spend exceeds 2x the 7-day average. This takes 30 minutes to build and can save thousands.
6. **Separate API keys per environment.** Dev, staging, and production should have different keys with different spending limits. A dev experiment should not be able to consume your production budget.

**Choose managed cost controls when:** Always. There is no scenario where "no spending limit" is the right answer.

**Avoid:** Sharing a single API key across environments. Deploying without spending caps. Running agent loops without maximum iteration limits.

---

## 5. The Simplicity Principle

The boring infrastructure that actually works is not exciting enough for conference talks. That is precisely why it works — nobody is building it for their portfolio.

### Why a VPS Beats the Cloud (for 95% of AI Practitioners)

A $20/month VPS with Docker Compose gives you:
- A single machine to SSH into and debug
- `docker compose up -d` deployment
- Predictable monthly cost
- Full control over data location
- No IAM policies, no VPC configuration, no load balancer setup

The same setup on AWS involves EC2, RDS, ECR, ALB, IAM, VPC, Security Groups, CloudWatch, and a monthly bill that requires a spreadsheet to understand. For a side project or early-stage product serving fewer than 1,000 users, this complexity adds zero value.

### Why cron + systemd Beats Airflow

Apache Airflow requires a metadata database (usually Postgres), a web server, a scheduler process, and worker processes. It is a distributed system. For complex data pipelines with 50+ interdependent tasks across multiple teams, it is excellent.

For running a Python script every hour that fetches data and updates a database, it is absurd. A cron job does this in one line:

```
0 * * * * /usr/bin/python3 /opt/scripts/fetch_data.py >> /var/log/fetch.log 2>&1
```

A systemd timer adds logging, restart-on-failure, and resource limits. Still one file. Still no metadata database.

**Choose Airflow when:** You have 20+ scheduled jobs with complex dependencies, multiple teams need visibility into job status, and you need retry logic with backfill capabilities.

**Avoid Airflow when:** You have fewer than 10 scheduled tasks, a single developer maintains them, and dependencies are linear. cron or systemd timers handle this with zero operational overhead.

### Why SQLite Beats Postgres (for Most AI Side Projects)

SQLite requires no server process, no configuration, no user management, and no network setup. Your database is a single file. Back it up with `cp`. Deploy it by copying the file. For a solo developer building an AI project that handles fewer than 100 concurrent writes per second, SQLite is not just simpler — it is faster for read-heavy workloads because there is no network round-trip.

**Choose Postgres when:** You need concurrent write access from multiple processes, full-text search at scale, or your data exceeds what fits comfortably on a single disk.

**Avoid Postgres when:** You are the only person reading and writing to the database, your dataset is under 10GB, and you do not need concurrent multi-process writes. SQLite eliminates an entire category of operational problems.

---

## 6. Infrastructure as Code for AI

Infrastructure as Code (IaC) — Terraform, Pulumi, CloudFormation — exists because manual infrastructure changes do not scale across teams. But "does not scale across teams" is the key qualifier.

### When IaC Is Overhead

A solo developer managing a single VPS does not need Terraform. The overhead of learning HCL syntax, managing state files, configuring backends, and debugging provider version mismatches exceeds the benefit. The VPS was provisioned once. It will be reprovisioned maybe twice in its lifetime. A documented checklist in a README accomplishes the same thing with less cognitive load.

### When IaC Matters

Once you have more than 3 people who can modify infrastructure, or more than 2 environments (dev, staging, production), or infrastructure that gets recreated regularly (CI/CD runners, ephemeral test environments), IaC prevents the "who changed what and when" problem. At that point, the investment pays off.

### The Practical Minimum

For most AI practitioners, the entire infrastructure definition fits in three files:

```yaml
# docker-compose.yml
services:
  app:
    build: .
    env_file: .env
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  vector-db:
    image: qdrant/qdrant:latest
    ports:
      - "127.0.0.1:6333:6333"  # localhost only!
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  qdrant_data:
```

```bash
# backup.sh
#!/bin/bash
DATE=$(date +%Y-%m-%d)
tar czf /backups/app-$DATE.tar.gz /app/data
curl -X POST "http://localhost:6333/snapshots" # Qdrant snapshot
find /backups -mtime +30 -delete              # Keep 30 days
```

```
# .env.example
OPENAI_API_KEY=sk-your-key-here
QDRANT_HOST=vector-db
QDRANT_PORT=6333
APP_PORT=3000
```

This is infrastructure as code. It is version-controlled. It is reproducible. It just does not require learning a domain-specific language or managing a state backend.

**Choose Terraform/Pulumi when:** Multiple team members modify infrastructure, you manage resources across multiple cloud providers, or you need audit trails for compliance.

**Avoid Terraform/Pulumi when:** You are a solo developer, you have a single VPS or cloud account, and your infrastructure changes less than once a month.

---

## Hype vs. Reality Scorecard

| Tool | Hype | Reality for AI Practitioners | Verdict |
|------|------|------------------------------|---------|
| **Kubernetes** | "Industry standard for deployment" | Requires dedicated platform team. 73% of clusters under 25% utilization. | Skip until you have 10+ services and a platform engineer. Use Docker Compose. |
| **Terraform** | "Infrastructure as Code is essential" | Steep learning curve, state management headaches, provider version conflicts. | Skip for solo dev on a single VPS. Use a documented setup checklist + docker-compose.yml. |
| **Airflow** | "Modern workflow orchestration" | Requires Postgres, webserver, scheduler, workers. A distributed system for running scripts. | Skip for fewer than 20 scheduled tasks. Use cron + systemd timers. |
| **LangChain** | "The framework for LLM applications" | Heavy abstraction layer, version instability, debugging opacity. | Start with raw API calls. Adopt LangChain only when you need its specific abstractions (agent routing, tool chaining at scale). |
| **Managed Vector DBs (Pinecone)** | "Serverless vector search" | Great for teams that do not want to manage infrastructure. Vendor lock-in, cost at scale. | Use self-hosted Qdrant/ChromaDB until you need multi-region or guaranteed uptime SLAs. |
| **MLOps Platforms (MLflow, W&B)** | "Track every experiment" | Valuable for ML teams. Overkill if you are calling APIs, not training models. | Skip if you are using hosted LLMs. Adopt if you are fine-tuning or training custom models. |
| **GitHub Actions CI/CD** | "Automate everything" | Genuinely useful. Simple YAML, free tier for public repos, integrates with everything. | Use it. One of the few "hyped" tools that delivers proportional value for solo devs. |
| **Docker** | "Containerize everything" | Solves real problems (environment reproducibility) with reasonable overhead. | Use it for anything you deploy. The Dockerfile tax is 30 minutes; the payoff is years. |

---

## Key Takeaways

1. **Infrastructure debt is worse than technical debt.** Wrong code can be refactored. Wrong infrastructure reshapes how you think about your product.
2. **The four-minute rule.** Leaked credentials on GitHub are found by bots within four minutes. Treat every accidental commit as an active breach.
3. **Set spending limits before writing code.** API budget caps, per-user rate limits, circuit breakers. These are not optimizations — they are requirements.
4. **Start with one machine.** VPS + Docker Compose + cron. Scale when the pain is real, not when the architecture diagram looks impressive.
5. **Security defaults are insecure.** Qdrant ships without auth. Flowise had a trivial bypass. Assume every default is wrong and configure security explicitly.
6. **Complexity is a cost.** Every tool you add is a tool you must maintain, debug, upgrade, and secure. Justify each one against the simplest alternative that works.

---

*Sources compiled from GitGuardian State of Secrets Sprawl 2024/2025, OWASP LLM Top 10 2025, Legit Security GenAI exposure research, Kubernetes failure compilations (k8s.af), and documented cloud billing incidents.*
