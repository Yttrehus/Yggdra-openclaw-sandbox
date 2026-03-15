# Chapter 9: Setup & Infrastructure — From Zero to Production

> "The best infrastructure is the one you forget about because it just works."

Most AI practitioners spend 80% of their time choosing tools and 20% deploying them. Invert that ratio. This chapter covers the infrastructure decisions that actually matter for AI-powered services, with real costs, real failure modes, and opinionated recommendations. No "it depends."

---

## 9.1 VPS vs Cloud Providers vs Serverless

The hosting decision is one of the first you make and one of the hardest to undo. Most solo developers and small teams are massively over-provisioned — running $200/month AWS setups for workloads that would run fine on a $5 VPS.

### The Three Tiers

**Tier 1: Budget VPS (Hetzner, DigitalOcean, Hostinger)**

A Hetzner CX22 gives you 2 vCPUs, 4GB RAM, 40GB NVMe SSD for **EUR 3.79/month** ([Hetzner Cloud Pricing](https://www.hetzner.com/cloud)). Their CX33 — 4 vCPUs, 8GB RAM — costs EUR 5.49/month. DigitalOcean's equivalent 4GB Droplet runs $24/month; Hostinger's KVM VPS starts around $4.49/month ([nucamp: Top 10 Low-Cost VPS 2026](https://www.nucamp.co/blog/top-10-low-cost-vps-providers-in-2026-affordable-alternatives-to-aws-azure-gcp-and-vercel)).

A 4GB VPS comfortably runs: a vector database (Qdrant with 50K+ vectors), a web application, a reverse proxy with SSL, multiple Python scripts, cron jobs, and a Tor proxy — simultaneously. This is not hypothetical; it is the actual production stack behind the Ydrasil project described in this book.

**Tier 2: Major Cloud Providers (AWS, GCP, Azure)**

AWS EC2 t3.medium (2 vCPUs, 4GB) costs ~$30/month on-demand. Add an RDS database ($15-50/month), a load balancer ($16/month), and S3 storage ($0.023/GB/month), and your "simple app" costs $80-150/month before you've served a single request. The pricing pages are intentionally complex. You will be surprised by your first bill.

The real cost of AWS is not compute — it is **cognitive overhead**. IAM policies, VPC configuration, security groups, CloudWatch alarms, billing alerts across 200+ services. A solo developer spends more time managing AWS than building features.

**Tier 3: Serverless (Lambda, Cloud Functions, Vercel)**

AWS Lambda charges $0.20 per million requests plus $0.0000166667 per GB-second of compute ([AWS Lambda Pricing](https://costgoat.com/pricing/aws-lambda)). For intermittent workloads — a webhook that fires 100 times a day, a scheduled daily job — this can cost literally nothing (free tier: 1M requests/month).

But serverless has a hidden cost for AI workloads: **cold starts and execution limits**. Lambda functions have a 15-minute maximum execution time and limited memory (up to 10GB). Loading a vector database, processing large documents, or running multi-step agent workflows simply does not fit this model. You end up architecting around the platform's limitations rather than solving your actual problem.

### The Decision

**Choose a VPS when:** You run always-on services (web apps, databases, APIs). You want full control. You are a solo developer or small team. Your monthly budget is under $50. This covers 90% of AI practitioners.

**Avoid a VPS when:** You need auto-scaling for unpredictable traffic spikes. You have compliance requirements that demand managed services with SLAs. You are a team of 10+ where DevOps overhead is shared.

**Choose serverless when:** Your workload is genuinely intermittent — webhook handlers, scheduled batch jobs, event-driven pipelines. You want zero maintenance for specific functions.

**Avoid serverless when:** You need persistent connections, long-running processes, or local state. AI agent workflows that run for minutes (not seconds) are a bad fit.

**Choose major cloud providers when:** You need managed databases with automated failover. Your team has dedicated ops/DevOps. You are spending $500+/month and need SLAs.

**Avoid major cloud providers when:** You are a solo practitioner. Your total infrastructure budget is under $100/month. You do not have someone whose job includes understanding the billing dashboard.

### Failure Modes

- **The AWS trap:** Starting with AWS "because that's what companies use." Three months later you're spending $120/month for infrastructure you could run on a $5 VPS, and you've spent 40 hours learning IAM instead of building your product.
- **The serverless trap:** Choosing Lambda for an AI workflow, then discovering your agent needs 20 minutes to complete a task. You architect an elaborate Step Functions state machine to work around the 15-minute limit. The state machine costs more than a VPS would have.
- **The Hetzner trap:** Choosing the cheapest VPS, skipping backups, and losing everything when the disk fails. Budget hosting is fine. Budget hosting without a backup plan is gambling.

---

## 9.2 The Self-Hosting Decision

Self-hosting is not a binary choice. It is a spectrum, and the correct answer is different for each component of your stack.

### What to Self-Host

**Vector databases: Self-host.** Qdrant runs in a single Docker container, uses ~200MB RAM for 50K vectors, and requires zero maintenance beyond occasional snapshots. Pinecone's managed service starts at $0.15/hour (~$108/month) for equivalent capacity ([Pinecone pricing](https://www.pinecone.io/pricing/)). Self-hosted Qdrant on a $5 VPS costs $5/month total — a 20x cost difference. At under 1M vectors, there is no reason to use a managed vector database.

**Web applications: Self-host.** An Nginx or Node.js server behind a reverse proxy is trivial to deploy with Docker. Vercel and Netlify are fine for static sites but charge premium prices the moment you need server-side logic, persistent connections, or custom runtimes.

**Automation workflows: Self-host.** n8n Community Edition is free with unlimited executions when self-hosted. The cloud version starts at $24/month for 2,500 executions ([n8n pricing](https://n8n.io/pricing/)). If you run 50+ automations daily — which is common once you start connecting AI to real workflows — self-hosting saves $300-800/year.

**Cron jobs and scripts: Self-host.** Systemd timers and cron on a VPS are free, reliable, and simple. Managed alternatives (AWS EventBridge, Cloud Scheduler) add cost and complexity for zero benefit at small scale.

### What Not to Self-Host

**LLM inference: Do not self-host** (unless you have dedicated GPUs). Running a 7B parameter model on a VPS CPU produces 2-3 tokens/second — unusable for interactive applications. An NVIDIA A100 GPU instance costs $1.10-3.00/hour on cloud providers. The API cost for equivalent Claude Sonnet usage is typically $5-30/month for a solo practitioner. Self-hosting LLMs only makes sense at high volumes (millions of tokens/day) or when you have dedicated GPU hardware.

**Email delivery: Do not self-host.** Email deliverability requires IP reputation, DKIM/SPF/DMARC configuration, and constant monitoring. Use SendGrid (free tier: 100 emails/day), Resend, or Postmark. The debugging time for self-hosted email exceeds the subscription cost within the first week.

**DNS: Do not self-host.** Cloudflare offers free DNS with DDoS protection, CDN, and global anycast. Running your own DNS server is a security liability with no upside.

**Databases with complex replication needs: Consider managed.** If your application requires multi-region replication, automated failover, or point-in-time recovery, managed databases (PlanetScale, Supabase, or RDS) earn their cost. For a single-node PostgreSQL or SQLite — self-host without hesitation.

### Choose When / Avoid When

**Choose self-hosting when:** The service is stateless or has simple state (files, single-node DB). You have a backup strategy. The managed alternative costs 5x+ more than your VPS. You want full data control.

**Avoid self-hosting when:** The service requires specialized expertise you don't have (email, DNS, distributed databases). The managed version has a free tier that covers your usage. Downtime costs you real money — revenue or reputation.

### Failure Modes

- **Over-self-hosting:** Running your own email server, DNS, and monitoring stack. You're now a sysadmin, not an AI practitioner.
- **Under-self-hosting:** Paying $50/month for managed Qdrant, $24/month for n8n cloud, and $20/month for managed PostgreSQL — $94/month for services that run perfectly on a single $5 VPS.
- **No backup self-hosting:** Self-hosting a vector database with 50K embeddings and no snapshot strategy. One corrupted disk, and you re-embed everything from scratch (hours of compute, $20+ in API costs).

---

## 9.3 Reverse Proxies & SSL

Every AI service you expose to the internet needs two things: a reverse proxy and SSL. Without SSL, API keys transit in plaintext. Without a reverse proxy, you expose application ports directly to the internet.

### The Three Options

**Caddy: The new default.** Automatic HTTPS out of the box. You write a three-line config file, point your domain at it, and Caddy obtains, provisions, and renews Let's Encrypt certificates automatically. HTTP/2 and HTTP/3 enabled by default. Zero-config SSL is not marketing — it is the actual experience ([Caddy Server](https://caddyserver.com/)).

```
app.example.com {
    reverse_proxy localhost:3000
}

api.example.com {
    reverse_proxy localhost:8080
}
```

That is a complete, production-ready config. Two domains, reverse proxied, with automatic SSL. Compare to the 40+ lines required for equivalent Nginx configuration.

**Traefik: The Docker-native option.** Traefik watches your Docker socket and automatically discovers services via container labels. You add a label to your container, and Traefik creates the route with SSL. Excellent for dynamic environments where containers come and go. More complex initial setup than Caddy, but unmatched Docker integration ([Traefik vs Caddy comparison](https://www.programonaut.com/reverse-proxies-compared-traefik-vs-caddy-vs-nginx-docker/)).

**Nginx: The legacy choice.** Still the highest-performance option for raw throughput. But manual SSL configuration with Certbot, manual renewal via cron, and verbose config files make it the worst choice for new projects. If you're already comfortable with Nginx, keep using it. If you're starting fresh, choose Caddy or Traefik.

### The Decision

**Choose Caddy when:** You want the simplest possible setup. You have a small number of services (1-10). You are not running Kubernetes. This is the right choice for most AI practitioners.

**Choose Traefik when:** You run Docker Compose or Docker Swarm with dynamic services. You want automatic service discovery from container labels. You might move to Kubernetes later.

**Avoid Nginx for new projects when:** You don't already have Nginx expertise. You don't need sub-millisecond proxy latency (you don't). The configuration complexity is not worth the performance gain for AI workloads.

### What Matters for AI Services

AI APIs often have long-running requests. An embedding batch might take 30 seconds. An agent workflow might stream for 2 minutes. Default proxy timeouts (60 seconds) will kill these requests silently. Always configure:

- **Proxy timeouts:** Set to 300 seconds minimum for AI-facing endpoints.
- **Request body limits:** Increase from the default 1MB to 10-50MB if you handle document uploads for RAG pipelines.
- **WebSocket support:** Required if you stream LLM responses to a frontend.
- **Rate limiting:** Protect your AI endpoints from abuse. A single bad actor can run up $500 in API costs through your proxy.

### Failure Modes

- **No SSL:** Your API key travels in plaintext. Someone on the same network captures it. They run $2,000 in API calls overnight.
- **Default timeouts:** Your RAG pipeline works in testing (small documents, fast responses). In production, large documents timeout silently at the proxy layer. Users see blank responses. Logs show nothing because the proxy dropped the connection before the app could respond.
- **Missing rate limiting:** You deploy an AI-powered API. Someone discovers it and sends 10,000 requests in an hour. Your OpenAI bill for that hour: $400.

---

## 9.4 Monitoring & Uptime

Monitoring for AI services is different from traditional web monitoring. Your app might return HTTP 200 while the LLM is hallucinating garbage, your vector database has stale embeddings, or your API costs are spiraling.

### The Minimum Viable Monitoring Stack

**Layer 1: External uptime monitoring (free).** UptimeRobot free tier gives you 50 monitors with 5-minute intervals ([UptimeRobot](https://uptimerobot.com/)). Monitor every public endpoint: your web app, your API, your webhook receivers. This catches "the server is down" and "the SSL cert expired." Set up alerts to Telegram, email, or Slack.

**Layer 2: Process monitoring (systemd + cron).** For services running as systemd units, `Restart=on-failure` handles automatic recovery. For cron jobs, pipe output to a log file and set up a simple checker that alerts if the job hasn't run in N hours:

```bash
# /etc/cron.d/health-check
0 * * * * root /usr/local/bin/check_services.sh | mail -s "Health Check" you@email.com
```

**Layer 3: Cost monitoring (API dashboards).** Check your OpenAI usage page weekly. Check your Anthropic usage page weekly. Set billing alerts at 50% and 80% of your monthly budget. This is the monitoring most practitioners skip — and the one that hurts most when ignored.

**Layer 4: Application health (custom endpoints).** Add a `/health` endpoint to every service that checks its actual dependencies:

```json
{
  "status": "ok",
  "qdrant": "connected",
  "qdrant_vectors": 50142,
  "last_embedding": "2026-02-09T08:15:00Z",
  "disk_free_gb": 24.3
}
```

Monitor this endpoint with UptimeRobot using keyword monitoring. If `"status": "ok"` disappears, you get alerted.

### Choose When / Avoid When

**Choose UptimeRobot + systemd + cron when:** You run 1-10 services on 1-3 servers. Your team is 1-3 people. This covers 95% of AI practitioners.

**Avoid this minimal stack when:** You have compliance requirements for audit trails. You need per-request tracing across multiple services. You run 50+ services.

**Choose Grafana + Prometheus when:** You need dashboards, historical metrics, and trend analysis. You are debugging performance issues across multiple services. You enjoy infrastructure work.

**Avoid Grafana when:** You are a solo developer. The time spent maintaining Grafana exceeds the time it saves you debugging issues. Most solo AI practitioners will never need it.

### Failure Modes

- **Monitoring the wrong thing:** Your uptime monitor says the web server is up. But the vector database crashed 3 hours ago, and every search returns zero results. Users see a working page with broken functionality.
- **No cost monitoring:** You add a new feature that sends 5x more tokens per request. Your daily API cost jumps from $3 to $15. You notice 12 days later when the monthly bill arrives: $180 instead of the expected $90.
- **Alert fatigue:** You set up 30 alerts for every possible failure. After two weeks of noise, you mute them all. The one real failure goes unnoticed.

---

## 9.5 Backup & Disaster Recovery

The question is not "will my VPS fail?" but "when my VPS fails, how fast can I recover?" Every hosting provider has outages. Disks fail. You will accidentally `rm -rf` the wrong directory at least once.

### What to Back Up in an AI Stack

**Critical (lose this, lose everything):**
- Configuration files: Docker Compose, systemd units, nginx/Caddy configs, .env files
- Application code and scripts (should be in Git — this IS your backup)
- Vector database snapshots (Qdrant: `curl -X POST localhost:6333/snapshots`)
- Credentials file (encrypted, stored separately)

**Important (expensive to recreate):**
- Embedded data: The raw documents/data BEFORE embedding. Re-embedding 50K documents costs $10-50 in API calls and hours of processing.
- Cron job definitions and automation configs
- SSL certificates (Caddy/Traefik regenerate these automatically, but it's nice to avoid the delay)

**Nice to have (inconvenient to lose):**
- Logs and session history
- Monitoring configurations
- Custom scripts and one-off tools

### The Minimum Backup Strategy

**Daily automated backup.** A cron job at 04:00 that:
1. Takes a Qdrant snapshot
2. Tars config files, scripts, and data directories
3. Pushes to an offsite location (a second VPS, S3, or Backblaze B2)

Backblaze B2 costs $0.005/GB/month for storage — a complete AI stack backup (configs + vector snapshots + scripts) is typically under 5GB, costing $0.025/month. There is no excuse for not having offsite backups.

**Weekly full-system snapshot.** Most VPS providers offer automated snapshots: Hetzner charges EUR 0.01/GB/month for snapshots, DigitalOcean charges $0.06/GB/month. A 40GB server snapshot costs EUR 0.40-2.40/month.

**Git as backup.** Every script, config template, and document in your project should be in a Git repository. Pushed to GitHub/GitLab, this is a free, versioned, distributed backup. Never store credentials in Git — use `.env` files listed in `.gitignore`.

### The "My VPS Dies" Recovery Plan

Write this down and test it once. Restoring should take under 2 hours:

1. Provision new VPS (5 minutes)
2. Clone Git repo (2 minutes)
3. Install Docker, restore Docker Compose stack (15 minutes)
4. Restore Qdrant snapshot from offsite backup (10-30 minutes)
5. Update DNS to point to new server (5 minutes + propagation)
6. Restore `.env` and credentials from encrypted backup (5 minutes)
7. Verify all services pass health checks (10 minutes)

If you cannot describe this process, you do not have a disaster recovery plan.

### Failure Modes

- **Backups on the same disk:** Your daily backup runs to `/root/backups/`. The disk fails. You lose the server AND the backups.
- **Untested backups:** You've been running daily backups for 6 months. The VPS fails. You try to restore and discover the Qdrant snapshot format changed 3 months ago and your backups are corrupt. Test restores quarterly.
- **Missing credentials backup:** The server dies. You restore everything from Git and backups. But your `.env` file with API keys, database passwords, and service tokens was only on the dead server. You spend a day resetting credentials across 8 services.

---

## 9.6 Cost Management

AI infrastructure costs spiral in ways traditional web infrastructure does not. A web server serves pages for the same cost regardless of content. An AI service's cost scales with usage, model choice, and — crucially — bugs.

### Where AI Costs Hide

**API costs (the big one).** Claude Sonnet: $3 input / $15 output per million tokens. GPT-4o: $2.50 input / $10 output per million tokens. OpenAI embeddings (text-embedding-3-small): $0.02 per million tokens ([Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing), [OpenAI pricing](https://openai.com/api/pricing/)). These sound cheap until you calculate actual usage:

- Embedding 50K documents (avg 500 tokens each) = 25M tokens = $0.50
- 100 RAG queries/day with Sonnet (avg 2K input + 500 output tokens) = $0.90/day input + $0.75/day output = **$49.50/month**
- One runaway agent loop that sends 500 requests before you notice = $25-75 in a single incident

**Infrastructure costs (predictable).** VPS: $5-50/month. Domain: $10-15/year. These are fixed and manageable.

**Storage costs (sneaky).** Vector embeddings grow. Session logs grow. Backups grow. A single Qdrant collection with 50K 1536-dimension vectors uses ~300MB. Manageable. But if you embed every conversation, every session log, every document — you can hit 10GB within a year. On S3, that is $0.23/month. On a VPS with limited disk, that is "time to resize."

### Cost Controls That Actually Work

**Hard spending limits.** Anthropic enforces monthly spend limits by tier ([Anthropic Usage Tiers](https://www.aifreeapi.com/en/posts/claude-api-quota-tiers-limits)). OpenAI offers budget alerts but not hard stops — their monthly budget limit was changed to an alert only, not a cutoff ([OpenAI Community](https://community.openai.com/t/monthly-budget-limit-silently-removed/1193635)). For OpenAI, build your own kill switch: a proxy that tracks cumulative daily spend and returns 429 when the limit is hit.

**Model routing.** Not every request needs your most expensive model. Route simple lookups to Haiku ($1/$5 per million tokens), standard tasks to Sonnet ($3/$15), and complex reasoning to Opus ($15/$75). A task router that classifies intent before choosing a model can reduce costs by 40-60% with negligible quality impact for the cheap tasks.

**Caching.** If users ask similar questions, cache the results. A simple hash of (query + relevant context) as a cache key eliminates duplicate API calls. Redis or even a JSON file works at small scale.

**Weekly cost reviews.** Every Sunday, check: Anthropic dashboard, OpenAI dashboard, VPS billing, any other paid service. Five minutes that prevents $200 surprises.

### The Budget Framework

| Monthly Budget | Recommended Stack |
|---|---|
| **$0-10** | Hetzner CX22 ($4), free-tier APIs, self-hosted everything |
| **$10-50** | Hetzner CX33 ($6), Anthropic/OpenAI API ($20-40), UptimeRobot free |
| **$50-200** | DigitalOcean/Hetzner ($10-20), API costs ($30-150), Backblaze B2 ($1), domain ($1) |
| **$200+** | Consider managed services for components where your time > hosting cost |

Most solo AI practitioners land in the $10-50/month range. If you are spending more than $100/month as a solo developer without paying customers, you are almost certainly over-provisioned.

### Failure Modes

- **The recursive agent:** Your AI agent calls itself in a loop. Each call costs $0.05. It runs 2,000 times before your rate limit kicks in. Cost: $100 in 20 minutes.
- **The embedding explosion:** You decide to embed all your session logs "for future retrieval." 100K chunks at $0.02/million tokens is cheap — but the daily re-embedding job you set up to "keep things fresh" re-embeds everything, every day. Cost: $0.50/day = $15/month for a "cheap" operation.
- **Model upgrade surprise:** You switch from Haiku to Sonnet "for better quality." Your daily cost goes from $2 to $12. Annualized difference: $3,650. Was the quality improvement worth it? You didn't measure before switching.
- **The staging environment:** You deploy a "test" environment that makes real API calls with real models. It runs for 3 months. Nobody uses it. Cost: $200 in API calls for testing that could have used mock responses.

---

## Summary: The Production Infrastructure Checklist

Before you deploy any AI service, verify:

- [ ] **Hosting:** VPS ($5-20/month) unless you have a specific reason for more
- [ ] **Reverse proxy:** Caddy or Traefik with automatic SSL. Never expose app ports directly.
- [ ] **Firewall:** UFW or equivalent. Allow only 22, 80, 443. Everything else bound to localhost.
- [ ] **Monitoring:** UptimeRobot (free) on every public endpoint. Systemd restart-on-failure for services.
- [ ] **Backups:** Daily automated to offsite storage. Tested quarterly. Credentials stored separately.
- [ ] **Cost alerts:** Set at 50% and 80% of monthly budget on every API provider.
- [ ] **Recovery plan:** Written, tested, achievable in under 2 hours.

This entire stack costs $5-30/month. It is production-grade. It handles 95% of solo practitioner and small team needs. Everything beyond this is optimization — valuable at scale, premature before product-market fit.

The infrastructure that matters most is not the infrastructure. It is the AI workflows running on top of it. Get the foundation right, then forget about it and build.

---

*Sources consulted: [Hetzner Cloud](https://www.hetzner.com/cloud), [DigitalOcean Droplets](https://www.digitalocean.com/pricing/droplets), [AWS Lambda Pricing](https://costgoat.com/pricing/aws-lambda), [Anthropic Pricing](https://docs.anthropic.com/en/docs/about-claude/pricing), [OpenAI API Pricing](https://openai.com/api/pricing/), [Caddy Server](https://caddyserver.com/), [UptimeRobot](https://uptimerobot.com/), [n8n Pricing](https://n8n.io/pricing/), [Qdrant vs Pinecone comparison (Ryz Labs)](https://learn.ryzlabs.com/rag-vector-search/pinecone-vs-weaviate-vs-qdrant-the-best-vector-database-for-rag-in-2026), [nucamp VPS Guide 2026](https://www.nucamp.co/blog/top-10-low-cost-vps-providers-in-2026-affordable-alternatives-to-aws-azure-gcp-and-vercel), [Nginx vs Caddy 2025](https://mangohost.net/blog/nginx-vs-caddy-in-2025-which-is-better-for-performance-and-tls-automation-2/), [Reverse Proxy Comparison (Programonaut)](https://www.programonaut.com/reverse-proxies-compared-traefik-vs-caddy-vs-nginx-docker/), [Backblaze B2 Pricing](https://www.backblaze.com/cloud-storage/pricing)*
