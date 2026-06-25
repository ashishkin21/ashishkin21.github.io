# Artem Shishkin
**QA Engineer (Backend) — SRE → QA Transition**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Backend QA engineer (SRE → QA transition) with 8 years ensuring system reliability, reproducing and localizing defects, and validating releases for a 40+ microservice banking platform at 99.9% uptime. Built release-readiness validators enforcing test-coverage and rollback gates (cut prep from 20+ min to <2 min), and ran online quality evaluation pipelines in production — Python, SQL, Kafka, GitLab CI/CD, Docker/Kubernetes. Currently ramping up on Go and test automation frameworks (testify, gomega); no production Go yet — closing that gap now.

---

## Skills

**Testing & Quality:** Test Automation, Test Scenarios, Test Data Preparation, Regression Testing, Acceptance Testing, Bug Reproduction & Reporting, Bug Tracking, Root Cause Analysis, Release Readiness Validation, pytest (basic, AI-assisted)
**Languages:** Python (8 yrs), SQL; Go (learning)
**Backend & APIs:** REST API, FastAPI, Pydantic, httpx, asyncio
**Data:** PostgreSQL, Oracle, SQL, Redis, Kafka
**Infrastructure & CI/CD:** Docker, Kubernetes, Helm, GitLab CI, Jenkins, Linux, HashiCorp Vault
**Observability:** Grafana, Graylog, Splunk, Kibana, Log Analysis, Monitoring, Alerts
**Auth & Security:** OAuth 2.0, Keycloak, JWT, JWKS, RS256
**Methodology & Tools:** Git, JIRA, Confluence, Service Desk, Agile, Scrum, SAFe, Kanban, Postmortems, Runbooks, On-Call

---

## Experience

### Automation Engineer — Home Credit International
**Remote | December 2023 – Present**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Engineered a **release-readiness validator** enforcing 3 pre-deploy gates — production rollback image in registry, new build image exists, and **test environment coverage complete** — then generates a dynamic release plan with pre-release, deployment, post-deploy verification, and rollback steps. Cut release prep from **20+ min to under 2 min per task across 10+ teams**.
- Implemented an **online quality evaluation pipeline** (RAGAS — Faithfulness, Groundedness, Instruction Adherence, scored by an LLM-as-a-judge in production) with retrieval-quality metrics logged on every call — continuous quality gating for production services.
- Built LLM resilience patterns (429 rate-limit priority escalation, automatic model fallback on exhausted retries) and streamed quality metrics to **Kafka** for downstream monitoring.
- Containerized **5+ internal tools** with Docker; deployed via **GitLab CI** to VMs and Kubernetes with Vault-managed secrets, structured JSON logging, and Grafana alerts.
- Secured APIs with **Keycloak JWKS/RS256** token verification.

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

- Sustained **99.9% uptime SLA** for a high-load banking platform (40+ microservices) in Kubernetes across production and test environments — the reliability-and-integration core backend QA is built on.
- Localized and resolved production incidents via **root cause analysis** — log forensics (Splunk, Graylog, Kibana), SQL (Oracle, PostgreSQL), metric correlation (Grafana) — the same investigation loop QA applies to defect localization.
- Built proactive Grafana/Splunk dashboards and alerts, reducing MTTD and catching defects before user impact.
- Conducted postmortems, maintained runbooks, and participated in on-call rotation.
- Automated deployment workflows via GitLab Pipelines and Jenkins, reducing deployment time and manual errors across 40+ services.
- Managed microservice configurations, Helm values, Vault secrets, and network access rules for 40+ services.

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided L2 technical support for high-load investment services (web and mobile apps) — investigated and resolved customer issues via Service Desk while maintaining resolution SLA.
- **Reproduced and documented bugs with logs and step-by-step reproduction, authoring bug reports escalated to development teams** — the closest equivalent to hands-on defect detection in my background.
- Escalated critical incidents to L3 and development teams with thorough diagnostic summaries, facilitating rapid resolution.
- Collaborated with frontend and backend developers to troubleshoot complex technical cases across the full stack.

---

## Projects

### Jira Release Readiness Validator
**Stack:** Python, FastAPI, Docker Registry API, Jira API

Validates release readiness across three gates: current production image exists in registry (rollback safety), new build image exists, and **test environment coverage is complete**. Generates a dynamic step-by-step release plan including pre-release steps, deployment steps, post-deploy verification resources, and rollback instructions. **Reduced release preparation time from 20+ minutes to under 2 minutes per task.** The most QA-adjacent project I've built — a validation harness enforcing pre-merge and pre-deploy quality gates.

### Automated Ticket Resolution & Root Cause Detection
**Stack:** Python, LangChain, RAG, Vector DB, Graylog, FastAPI, N8N

Parses and analyzes ticket descriptions, logs, and screenshots. For non-standard cases, searches a vectorized knowledge base for relevant documentation and API methods, queries Graylog logs, detects root cause, and auto-publishes validated solutions. **Solves ~15% of tickets automatically** — saves an estimated 200+ hours/month of support engineer time. Demonstrates the investigation loop — log analysis, evidence gathering, root cause detection — that backend QA applies to defect localization.

### Service Desk AI Agent Platform
**Stack:** Python, FastAPI, LangGraph, Kafka, Keycloak (JWKS), LDAP/AD, PostgreSQL, Docker, GitLab CI, Helm/Kubernetes

No-code AI agent platform handling 2000+ tasks/day with online RAGAS evaluation; winner of "Best IT Project of 2025." Included as evidence of building quality-measured backend services at scale — not as direct QA experience.

---

## Certificates
- **n8n Course** — Level 1 | [Certificate](https://community.n8n.io/badges/104/completed-n8n-course-level-1?username=shishkin) | December 2025
- **n8n Course** — Level 2 | [Certificate](https://community.n8n.io/badges/105/completed-n8n-course-level-2?username=shishkin) | December 2025
- **Back End Development and APIs** — freeCodeCamp | [Certificate](https://www.freecodecamp.org/certification/shishkin/back-end-development-and-apis) | July 2023
- **JavaScript Algorithms and Data Structures** — freeCodeCamp | [Certificate](https://www.freecodecamp.org/certification/shishkin/javascript-algorithms-and-data-structures) | February 2023

---

## Education

**Specialist, Marketing** — Russian State Social University (2012)

*Self-taught developer — transitioned from marketing analytics to software engineering through hands-on learning and certifications. Now moving from SRE/automation into backend QA, with focused study of Go and test automation frameworks.*
