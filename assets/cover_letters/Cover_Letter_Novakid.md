Hi Novakid team,

I'm applying for the AI engineer role. I'll be direct about the gaps first: I don't have 5+ years of pure production-software shipping in the classical sense, and my infra is Kubernetes/on-prem (Vault, Helm, GitLab CI) rather than AWS/GCP. If those are hard lines, feel free to stop reading here.

If they're not — here's what I _do_ bring, and why I'm writing anyway.

I've shipped 5+ AI-powered internal tools to production at Home Credit, used by 10+ teams. The flagship is a no-code AI agent platform integrated with Service Desk that now handles 2000+ tasks/day and won "Best IT Project of 2025". It's not a demo — it's what people open every morning.

Concretely, against the role:  

- **Architect the harness / design the agents:** LangGraph agents with parallel context aggregation (Send API) across Confluence, vector KBs, and logs; multi-prompt orchestration loop with live task-state refresh; access-controlled RAG filtered by Active Directory groups.  
- **Pick the models:** OpenAI-compatible APIs + self-hosted Qwen, with resilience built in — 429 priority escalation, automatic model fallback on exhausted retries.  
- **Run the evals:** RAGAS online — Faithfulness, Groundedness, Instruction Adherence scored by LLM-as-a-judge in production, plus retrieval-quality metrics on every RAG call. I ship on evals, not vibes.  
- **Wire up the tools / ship / improve:** Docker, GitLab CI → VMs + Kubernetes, structured JSON logging, Kafka metrics, Grafana alerts. ~15% of support tickets auto-resolved by a companion app, saving 200+ hours/month.  

I'm a power user of agentic coding tools — I build with AI, not around it. On frameworks: my strong opinion today is LangGraph + RAGAS over "just chain some prompts", and I'm self-aware enough to know that shifts in six months.

Small team, real ownership, ship-to-real-users is exactly the shape of work I want. Happy to talk specifics — the best demo is the system that's been live at 2000 tasks/day for months.

Artem Shishkin  
https://linkedin.com/in/ashishkin21 | https://t.me/ashishkin21
