# Artem Shishkin
**Python Developer — Internal Tools & AI Automation**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Delivered 5+ AI-powered internal tools and automations serving 2000+ tasks/day across multiple teams — saving 200+ hours/month of manual work. Built a no-code AI agent platform that won "Best IT Project of 2025". Python developer with 8 years in tech, specialized in LLM-based automation, RAG architectures, and internal tooling with FastAPI, LangChain/LangGraph, Docker, and CI/CD. Looking for a role focused on internal tooling and AI-powered automation.

---

## Skills

**Languages & Core:** Python, SQL, asyncio, REST API  
**Backend:** FastAPI, pydantic, httpx  
**AI & LLM:** LangChain, LangGraph, RAG, Prompt Engineering, Context Engineering, OpenAI-compatible APIs, Vector Databases, Embeddings
**Internal Tools:** N8N, workflow design, requirements gathering, process automation  
**Data:** PostgreSQL, Redis
**Infrastructure:** Docker, Kubernetes, Helm, GitLab CI, Linux, HashiCorp Vault  
**Observability:** Grafana, Graylog, Splunk, Kibana  
**Auth & Security:** OAuth 2.0, Keycloak  
**Methodology:** Agile, Scrum, SAFe, Kanban  
**Tools:** Git, JIRA, Confluence, AI-assisted development

---

## Experience

### Automation Engineer — Home Credit International
**Remote | December 2023 – Present**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Designed, built, and deployed 5+ internal tools and AI-powered automation apps from scratch to production, serving 10+ teams and eliminating hundreds of hours of manual work monthly
- Built a no-code AI agent platform integrated with Service Desk — handles 2000+ tasks/day via webhooks, LLM processing, and dynamic prompt catalog; won **"Best IT Project of 2025"** company award
- Developed RAG-based automated ticket resolution system that auto-resolves ~15% of support tickets and saves **200+ engineering hours/month**
- Created Jira release validator that automates pre-deployment checks and generates step-by-step release plans — reduced release preparation from **20+ minutes to under 2 minutes per task**
- Built Service Desk reporting tool with real-time aggregation, CSV exports, and LLM-powered improvement analysis; auto-delivers reports to stakeholders via messenger and email
- Containerized all applications with Docker, deployed via GitLab CI pipelines to VMs and Kubernetes with Vault-managed secrets
- Integrated apps with internal services via Keycloak-based OAuth 2.0 authentication
- Implemented custom logging, metrics, Grafana dashboards, and alerts for all applications

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

- Maintained 99.9% uptime for a high-load banking platform (40+ microservices) running in Kubernetes across production and test environments
- Managed microservice configurations, Helm values, Vault secrets, and network access rules for 40+ services
- Automated deployment workflows via GitLab Pipelines and Jenkins, reducing deployment time and manual errors
- Built proactive monitoring dashboards and alerts using Grafana, Splunk, Graylog, and Kibana — enabled early incident detection before user impact
- Performed root cause analysis via SQL queries in Oracle and PostgreSQL databases, resolving production incidents
- Worked within Agile frameworks including Scrum, SAFe, and Kanban across cross-functional teams

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided technical support for high-load investment services (web and mobile apps) serving a large active user base
- Investigated, diagnosed, and resolved customer issues via Service Desk — maintained high customer satisfaction and resolution SLA
- Escalated critical bugs and product improvement suggestions directly to development teams, contributing to product quality
- Collaborated with developers to troubleshoot and resolve complex technical cases across frontend and backend systems

---

## Projects

### Service Desk AI Agent
**Stack:** Python, FastAPI, LangChain, LangGraph, PostgreSQL, Docker, GitLab CI, N8N

No-code AI agent builder enabling non-technical users to create custom agents for any ticket form. Listens to task update webhooks, selects prompts from a dynamic catalog, enriches LLM context with documentation from Confluence, vector knowledge bases, and Graylog logs, then delivers structured results back. Built with LangGraph agents for intelligent parallel context aggregation.

Handles **2000+ tasks/day** regardless of type. **Winner of "Best IT Projects of 2025"** internal company award.

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

### App Store Ratings & Reviews
**Stack:** Python, requests, Grafana, App Store APIs, Web Scrapping

Collects and analyzes ratings and reviews from App Store, Galaxy Store, AppGallery for multiple company apps. Generates Grafana dashboard metrics and triggers automated alerts when app ratings decline.

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
