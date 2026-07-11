# Artem Shishkin
**AI Engineer — LLM Applications, Safety & Evaluation**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Built 5+ LLM applications and automations serving 2000+ tasks/day across multiple teams. Shipped a no-code AI agent platform (winner, Best IT Project of 2025) with online LLM evaluation (RAGAS, LLM-as-a-judge) running in production. Works with high autonomy in loosely-defined environments — owns products across the full SDLC (requirements → production reliability) and acts as a technical reference point for the team. AI Engineer with 9 years in tech, specialized in LLM applications, agentic workflows (LangGraph), RAG architectures, and production LLM evaluation using FastAPI, LangChain/LangGraph, and Docker. Hands-on with LLM-specific adversarial and defensive engineering: access-controlled retrieval (data leakage prevention), rate-limit and resource-abuse mitigation, API security (JWKS/RS256), and automated safety evaluation as a production gate.

---

## Skills

**LLM Safety & Security:** Access-controlled retrieval (data/context leakage prevention), rate-limit & resource/token-cost abuse mitigation, API security (Keycloak JWKS/RS256, OAuth 2.0), LLM evaluation for safety (RAGAS, LLM-as-a-Judge)  
**Languages & Backend:** Python, SQL, asyncio, REST API, FastAPI, Pydantic, httpx  
**AI & LLM:** LangChain, LangGraph (StateGraph, Send API, parallel agents), RAG (semantic search, access-controlled retrieval), Tool/function calling, RAGAS, LLM-as-a-Judge, LLM Evaluation, Prompt Engineering, OpenAI-compatible APIs, Self-hosted LLMs (Qwen3.6-35B-A3B-FP8, Qwen3.5-122B, Qwen3-235B-IT), Qdrant, Jay Knowledge Hub, Embeddings, Structured output validation, Context window management  
**Internal Tools:** N8N, workflow design, requirements gathering, process automation, LDAP / Active Directory  
**Data:** PostgreSQL, Redis, Kafka  
**Infrastructure:** Docker, Kubernetes, Helm, GitLab CI, Linux, HashiCorp Vault  
**Observability:** Grafana, Graylog, Splunk, Kibana  
**Auth & Security:** OAuth 2.0, Keycloak, JWT, JWKS, RS256  
**Tools & Methodology:** Git, JIRA, Confluence, pytest, Postman, httpx, python-docx, AI-assisted development, Agile, Scrum, SAFe, Kanban  

---

## Experience

### Automation Engineer — Sovcombank Technologies
**Remote | December 2023 – Present**

*Sovcombank Technologies — The dedicated IT and fintech subsidiary of a top-5 national commercial banking group, developing high-load internal platforms and applications for over 11 million active clients*

- Designed, built, and deployed 5+ LLM applications and automation tools from scratch to production, serving 10+ teams
- Owned each product across the full SDLC — operated with high autonomy in a loosely-defined environment: gathered requirements from stakeholders, made architectural and implementation decisions, set own priorities, and was accountable for production outcomes
- Acted as technical reference point for the team — advised on nearly all technical tasks, reviewed approaches, and co-implemented complex features to unblock teammates
- Built a no-code AI agent platform integrated with Service Desk — handles 2000+ tasks/day via webhooks, LLM processing, and dynamic prompt catalog
- Shipped online LLM evaluation in production with **RAGAS** — Faithfulness, Groundedness, and Instruction Adherence scored by an **LLM-as-a-judge** on every run, plus retrieval-quality metrics logged on every RAG call
- Built **LangGraph agents** with parallel context aggregation (Send API) across Confluence, knowledge bases, and log systems; multi-prompt orchestration loop with live task-state refresh
- Enforced **access-controlled RAG** — retrieved knowledge chunks filtered by user's Active Directory groups for per-role knowledge access (defense against data/context leakage)
- Engineered LLM resilience (429 rate-limit priority escalation, automatic model fallback on exhausted retries) — mitigation of resource and token-cost abuse
- Secured APIs with **Keycloak JWKS/RS256** token verification and **OAuth 2.0** authentication
- Owned product health beyond business logic — codebase quality, infrastructure, and reliability: containerized with Docker, deployed via GitLab CI to VMs/Kubernetes with Vault-managed secrets, structured JSON logging, and Grafana alerts

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Maintained 99.9% uptime for a high-load banking platform (40+ microservices) in Kubernetes; managed Helm values, Vault secrets, and network access rules for 40+ services
- Automated deployment workflows via GitLab Pipelines and Jenkins, reducing deployment time and manual errors
- Built proactive monitoring dashboards and alerts using Grafana, Splunk, Graylog, and Kibana — enabled early incident detection before user impact
- Performed root cause analysis via SQL queries in Oracle and PostgreSQL databases, resolving production incidents; authored postmortems with reproducible findings

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided technical support for high-load investment services (web and mobile apps), investigating and resolving customer issues via Service Desk while maintaining high satisfaction and resolution SLA
- Escalated critical bugs to development teams and collaborated across frontend and backend systems to troubleshoot complex technical cases
- Collected logs, reproduced bugs step-by-step, and authored bug reports with reproduction steps for development teams

---

## Projects

### Service Desk AI Agent
**Stack:** Python, FastAPI, LangGraph, Qwen (3.6-35B, 3.5-122B), Qdrant, Jay Knowledge Hub, RAGAS, Kafka, Keycloak (JWKS), LDAP/AD, PostgreSQL, Docker, GitLab CI, Helm/Kubernetes, N8N

No-code AI agent builder enabling non-technical users to create custom agents for any ticket form. Listens to task-update webhooks, selects prompts from a dynamic registry, enriches LLM context from Confluence, a corporate RAG service (Jay Knowledge Hub), Qdrant, and logs, then delivers structured results back via ticket comments, task fields, email (with DOCX attachments), and corporate messenger.

Architected with **LangGraph agents** using parallel context aggregation (Send API) across multiple sources, with **RAGAS** online evaluation (LLM-as-a-judge: Faithfulness, Groundedness, Instruction Adherence) running on every run. Retrieved chunks are **filtered by user's Active Directory groups** for per-role access (data leakage prevention). A multi-prompt orchestration loop advances tasks across workflow steps with live state refresh. Handles **2000+ tasks/day**.

### Jira Task Validator
**Stack:** Python, FastAPI, Docker Registry API, Jira API

Retrieves Jira release tasks and validates deployment readiness across 3 checks: current production image exists in registry (rollback safety), new build image exists, and test environment coverage is complete. Generates a dynamic step-by-step release plan including pre-release steps, deployment steps, post-deploy verification resources, and rollback instructions.

**Reduced release preparation time from 20+ minutes to under 2 minutes per task.**

---

## Certificates
- **n8n Course** — Level 1 | [Certificate](https://community.n8n.io/badges/104/completed-n8n-course-level-1?username=shishkin) | December 2025
- **n8n Course** — Level 2 | [Certificate](https://community.n8n.io/badges/105/completed-n8n-course-level-2?username=shishkin) | December 2025
- **Back End Development and APIs** — freeCodeCamp | [Certificate](https://www.freecodecamp.org/certification/shishkin/back-end-development-and-apis) | July 2023
- **JavaScript Algorithms and Data Structures** — freeCodeCamp | [Certificate](https://www.freecodecamp.org/certification/shishkin/javascript-algorithms-and-data-structures) | February 2023

---

## Education

**Specialist, Marketing** — Russian State Social University (2012)

*Self-taught developer — transitioned from marketing analytics to software engineering through hands-on learning and certifications.*
