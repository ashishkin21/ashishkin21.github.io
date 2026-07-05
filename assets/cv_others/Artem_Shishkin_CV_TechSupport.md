# Artem Shishkin
**Technical Support Engineer — L2**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Technical Support Engineer (L2) with 9 years as the bridge between users and engineering — triage, RCA, bug reproduction, and bug reports developers trust, across high-load, mobile, and fintech platforms. Investigates with SQL (PostgreSQL, Oracle), log forensics (Splunk, Graylog, Kibana), and API tools (Postman, REST); escalates only after root cause is understood. Bonus: ships support-automation in Python/N8N that takes the repetitive edge off L2 — including a platform handling 2000+ tasks/day.

---

## Skills

**Support & Incident Management:** L2/L3 Support, Triage, Bug Reproduction, Bug Reporting, Escalation Discipline, SLA Management, Root Cause Analysis, Postmortems, Runbooks, On-Call, Async Coverage, Handovers, Technical Documentation, Knowledge Base  
**Investigation Toolkit:** SQL (PostgreSQL, Oracle), Log Analysis (Splunk, Graylog, Kibana), API Tools (Postman, httpx, REST), Payment/Transaction Troubleshooting (fintech domain)  
**Infrastructure & Monitoring:** Linux, Network Diagnostics, Docker, Kubernetes, Grafana, HashiCorp Vault, GitLab CI, CI/CD  
**Automation & Scripting (bonus):** Python, FastAPI, N8N, LangChain, asyncio — support automation / vibe-coding  
**Data:** PostgreSQL, Oracle, Redis, Kafka, SQL  
**Security:** OAuth 2.0, Keycloak  
**Methodology & Tools:** Agile, Scrum, SAFe, Kanban, Git, JIRA, Confluence, Service Desk  

---

## Experience

### Automation Engineer — Sovcombank Technologies
**Remote | December 2023 – Present**  

*Technical support automation & tooling*  

*Sovcombank Technologies — The dedicated IT and fintech subsidiary of a top-5 national commercial banking group, developing high-load internal platforms and applications for over 11 million active clients*

- Powered **internal support for 10+ teams as customers** — owned 5+ internal tools end-to-end from requirements to production, resolving support issues with high autonomy
- Automated away **2000+ support tasks/day** via a no-code Service Desk platform — ticket triage, LLM-powered routing, and dynamic resolution; cut manual triage load across the org and won **"Best IT Project of 2025"**
- **Auto-resolved ~15% of incoming tickets** with a RAG system that searches vectorized knowledge bases and Graylog logs, identifies root cause, and publishes validated solutions — saved **~200 engineering hours/month**
- Cut release prep from **20+ min to under 2 min per task across 10+ teams** with a pre-deploy readiness validator (rollback image in registry, new build, test-coverage gates) plus a dynamic release plan with rollback steps
- Owned service health on-call — structured JSON logging and Grafana alerts; secured APIs with Keycloak JWKS/RS256 token verification

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Held **99.9% uptime SLA across 40+ microservices** in Kubernetes as **L3 escalation point** and incident responder for production and test environments
- Localized production incidents via RCA — log forensics (Splunk, Graylog, Kibana), SQL on Oracle/PostgreSQL, and metric correlation (Grafana)
- Reduced mean time to detection with proactive Grafana/Splunk/Graylog/Kibana dashboards and alerts — surfaced incidents before user impact
- Ran **on-call rotation 24/7**, authored postmortems and runbooks — async and night-shift discipline
- Managed Helm values, Vault secrets, and network access rules for 40+ services; automated deployments via GitLab Pipelines and Jenkins

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Delivered L2 support for high-load investment services across **web and mobile (iOS/Android)** — triaged connectivity, authentication, sync, and transaction issues to SLA and CSAT targets
- Reproduced bugs from logs, documented step-by-step reproduction, and authored **bug reports developers acted on** — escalated to L3/dev with diagnostic summaries that sped resolution
- Reduced repeat tickets by building internal knowledge base and support documentation
- Troubleshot full-stack cases alongside frontend and backend developers

---

## Projects

### Support Triage & Auto-Resolution Platform
**Stack:** Python, FastAPI, LangChain, Qdrant, Graylog, PostgreSQL, Keycloak (JWKS), LDAP/AD, Docker, GitLab CI, N8N

No-code platform handling **2000+ tasks/day** via Service Desk webhooks. Listens to ticket-update events, auto-selects a resolution flow from a dynamic catalog, enriches context from Confluence, vectorized knowledge bases, and Graylog logs, then returns structured results via ticket comments, task fields, and corporate messenger. **Winner of "Best IT Project of 2025"** — built the triage and resolution loop L2 works in every day.

### Automated Ticket Resolution & Root Cause Detection
**Stack:** Python, LangChain, RAG, Vector DB, Graylog, FastAPI, N8N

RAG-based auto-resolution for support tickets. Parses ticket descriptions, logs, and screenshots; searches a vectorized knowledge base for documentation and API methods; queries Graylog for error patterns; identifies root cause and auto-publishes validated solutions. **Auto-resolves ~15% of tickets** — saves an estimated **200+ hours/month**. Same investigation loop L2 applies to every non-trivial case: gather evidence from logs, localize, resolve.

### Service Desk Monitoring & Reporting
**Stack:** Python, PostgreSQL, N8N

Real-time support metrics with daily, weekly, and monthly CSV exports and visualizations. Auto-delivers reports to stakeholders via corporate messenger and email; LLM-driven ticket-trend analysis with actionable recommendations for support leads.

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
