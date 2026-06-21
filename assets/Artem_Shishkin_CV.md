# Artem Shishkin
**Python Developer — Internal Tools & AI Automation**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Delivered 5+ AI-powered internal tools and automations serving 2000+ tasks/day across multiple teams — saving 200+ hours/month of manual work. Built a no-code AI agent platform that won "Best IT Project of 2025", with online LLM evaluation (RAGAS, LLM-as-a-judge) running in production. Python developer with 8 years in tech, specialized in LLM-based automation, RAG architectures, LLM evaluation, and internal tooling with FastAPI, LangChain/LangGraph, Docker, and CI/CD.

---

## Skills

**Languages & Backend:** Python, SQL, asyncio, REST API, FastAPI, Pydantic, httpx  
**AI & LLM:** LangChain, LangGraph (StateGraph, Send API, parallel agents), RAG, RAGAS, LLM-as-a-Judge, LLM Evaluation, Prompt Engineering, Context Engineering, OpenAI-compatible APIs, Self-hosted LLMs (Qwen), Semantic Search, Vector Knowledge Bases, Embeddings  
**Internal Tools:** N8N, workflow design, requirements gathering, process automation, LDAP / Active Directory  
**Data:** PostgreSQL, Redis, Kafka  
**Infrastructure:** Docker, Kubernetes, Helm, GitLab CI, Linux, HashiCorp Vault  
**Observability:** Grafana, Graylog, Splunk, Kibana  
**Auth & Security:** OAuth 2.0, Keycloak, JWT, JWKS, RS256  
**Tools & Methodology:** Git, JIRA, Confluence, pytest, python-docx, AI-assisted development, Agile, Scrum, SAFe, Kanban  

---

## Experience

### Automation Engineer — Home Credit International
**Remote | December 2023 – Present**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Designed, built, and deployed 5+ internal tools and AI-powered automation apps from scratch to production, serving 10+ teams and eliminating hundreds of hours of manual work monthly
- Built a no-code AI agent platform integrated with Service Desk — handles 2000+ tasks/day via webhooks, LLM processing, and dynamic prompt catalog; won **"Best IT Project of 2025"** company award
- Implemented online LLM evaluation pipeline with **RAGAS** — Faithfulness, Groundedness, and Instruction Adherence scored by an **LLM-as-a-judge** in production, plus retrieval-quality metrics logged on every RAG call
- Built **LangGraph agents** with parallel context aggregation (Send API) across Confluence, knowledge bases, and log systems; multi-prompt orchestration loop with live task-state refresh
- Enforced **access-controlled RAG** — retrieved knowledge chunks filtered by user's Active Directory groups for per-role knowledge access
- Engineered LLM resilience (429 rate-limit priority escalation, automatic model fallback on exhausted retries), streamed bot metrics to **Kafka**, and secured APIs with **Keycloak JWKS/RS256** token verification
- Containerized all applications with Docker, deployed via GitLab CI pipelines to VMs and Kubernetes with Vault-managed secrets, structured JSON logging, and Grafana alerts

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

- Maintained 99.9% uptime for a high-load banking platform (40+ microservices) in Kubernetes; managed Helm values, Vault secrets, and network access rules for 40+ services
- Automated deployment workflows via GitLab Pipelines and Jenkins, reducing deployment time and manual errors
- Built proactive monitoring dashboards and alerts using Grafana, Splunk, Graylog, and Kibana — enabled early incident detection before user impact
- Performed root cause analysis via SQL queries in Oracle and PostgreSQL databases, resolving production incidents

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided technical support for high-load investment services (web and mobile apps), investigating and resolving customer issues via Service Desk while maintaining high satisfaction and resolution SLA
- Escalated critical bugs to development teams and collaborated across frontend and backend systems to troubleshoot complex technical cases

---

## Projects

### Service Desk AI Agent
**Stack:** Python, FastAPI, LangGraph, RAGAS, Kafka, Keycloak (JWKS), LDAP/AD, PostgreSQL, Docker, GitLab CI, Helm/Kubernetes, N8N

No-code AI agent builder enabling non-technical users to create custom agents for any ticket form. Listens to task-update webhooks, selects prompts from a dynamic registry, enriches LLM context with documentation from Confluence, vector knowledge bases, and logs, then delivers structured results back via ticket comments, task fields, email (with DOCX attachments), and corporate messenger.

Powered by **LangGraph agents** with parallel context aggregation (Send API) and **RAGAS** online evaluation (LLM-as-a-judge: Faithfulness, Groundedness, Instruction Adherence). Retrieved chunks are **filtered by user's Active Directory groups** for per-role access. A multi-prompt orchestration loop advances tasks across workflow steps with live state refresh. Handles **2000+ tasks/day**. **Winner of "Best IT Project of 2025"** internal company award.

### Automated Ticket Resolution App
**Stack:** Python, LangChain, RAG, Vector DB, Graylog, FastAPI, N8N

Parses and analyzes ticket descriptions, logs, and screenshots. For non-standard cases, searches a vectorized knowledge base for relevant documentation and API methods, queries Graylog logs, detects root cause, and auto-publishes validated solutions into the ticket system.

**Solves ~15% of tickets automatically** — saves an estimated **200+ hours/month** of support engineer time.

### Jira Task Validator
**Stack:** Python, FastAPI, Docker Registry API, Jira API

Retrieves Jira release tasks and validates deployment readiness across 3 checks: current production image exists in registry (rollback safety), new build image exists, and test environment coverage is complete. Generates a dynamic step-by-step release plan including pre-release steps, deployment steps, post-deploy verification resources, and rollback instructions.

**Reduced release preparation time from 20+ minutes to under 2 minutes per task.**

### Service Desk Reporting Tool
**Stack:** Python, PostgreSQL, LLM

Aggregates ticket data in real time, stores in a database, and generates daily/weekly/monthly reports with CSV exports and pie chart visualizations. Auto-sends reports via corporate messenger and email groups. LLM analyzes exported reports and generates improvement suggestions, highlighting problematic service areas.

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
