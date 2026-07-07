# Artem Shishkin
**SRE / DevOps Engineer**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Site Reliability Engineer with 4.5+ years across on-prem Kubernetes and CI/CD. In my current role I own end-to-end deployment of internal services — writing GitLab CI pipelines, preparing Helm/Docker/Vault infrastructure, deploying across environments, and supporting them in production. Prior SRE experience running a 40+ microservice banking platform adds on-call, incident response, and monitoring. Now transitioning into a dedicated DevOps role.
Stack: Kubernetes/Helm, Docker, Linux, GitLab CI/CD, Vault, Grafana, PostgreSQL, Oracle, Redis, Kafka — scripted in Python and Bash.

---

## Skills

**Infrastructure & Orchestration:** Kubernetes, Helm, Docker, Linux, HashiCorp Vault, Ingress, Network Policies, On-prem infrastructure (VMs, Kubernetes clusters)  
**CI/CD & Deployment:** GitLab Pipelines (editing, writing simple pipelines), Helm Charts, Ansible (Basic)  
**Scripting:** Python, SQL  
**Data:** PostgreSQL, Oracle, Redis, Kafka  
**Observability:** Grafana, Prometheus / VictoriaMetrics, ELK (Kibana), Splunk, Graylog, Structured JSON Logging  
**Security:** HashiCorp Vault, Keycloak, JWT/JWKS (RS256), OAuth 2.0  
**Methodology & Tools:** Git, JIRA, Confluence, Agile, Scrum, SAFe, Kanban  

---

## Experience

### Automation Engineer — Sovcombank Technologies
**Remote | December 2023 – Present**

*Sovcombank Technologies — The dedicated IT and fintech subsidiary of a top-5 national commercial banking group, developing high-load internal platforms and applications for over 11 million active clients*

- Owned 5+ internal platform services end-to-end — from requirements through deployment across environments, production operation, and user support — eliminating 200+ hours/month of manual work across 10+ teams
- Wrote GitLab CI/CD pipelines to containerize services with Docker and deploy them to VMs and Kubernetes, with HashiCorp Vault-managed secrets and structured JSON logging
- Prepared deployment infrastructure — Helm charts and values, ingress, and service-to-service network policies — for services across environments
- Built an internal automation platform handling 2000+ tasks/day via webhooks — engineered resilience with rate-limit priority escalation and automatic fallback on exhausted retries, and streamed service metrics to **Kafka** for observability and incident triage
- Configured **Grafana** dashboards and alerts for service health and latency, and secured APIs with **Keycloak JWKS/RS256** token verification
- Won **"Best IT Project of 2025"** company award for a no-code internal platform adopted across 10+ teams

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Operated **on-prem infrastructure** (VMs, Kubernetes clusters) for a high-load banking platform of 40+ microservices across production and test environments
- Supported the production application operationally — restarted pods, investigated errors from logs, and adjusted service configurations
- Deployed releases to production by triggering CI/CD pipelines and performed rollbacks by redeploying previous images (on test environments developers self-deployed via CI/CD)
- Participated in **on-call rotation** — reacted to alerts, triaged production incidents, and performed root cause analysis via SQL queries in **Oracle** and **PostgreSQL**
- First point of contact for development and QA teams — diagnosed test-environment deploy failures, database connectivity issues, and service-to-service communication problems
- Maintained **Helm values**, **Vault secrets**, network policies, and ingress for 40+ services within an existing Kubernetes setup
- Edited existing **GitLab CI** pipelines and wrote simple new ones; used Jenkins jobs for deployments
- Wrote **Dockerfiles** for services and maintained monitoring dashboards using **Prometheus / VictoriaMetrics**, Grafana, Splunk, Graylog, and Kibana
- Authored technical documentation for operational procedures and service onboarding

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided technical support for high-load investment services (web and mobile apps), investigating and resolving customer issues via Service Desk while maintaining resolution SLA
- Triaged incidents, collected and analyzed logs, and escalated critical cases to development teams with thorough diagnostic summaries

---

## Projects

### Jira Task Validator (Deployment Readiness)
**Stack:** Python, FastAPI, Docker Registry API, Jira API

Retrieves Jira release tasks and validates deployment readiness across 3 checks: current production image exists in registry (rollback safety), new build image exists, and test environment coverage is complete. Generates a dynamic step-by-step release plan including pre-release steps, deployment steps, post-deploy verification resources, and rollback instructions. **Reduced release preparation time from 20+ minutes to under 2 minutes per task.**

### Internal Automation Platform
**Stack:** Python, FastAPI, Kafka, Keycloak (JWKS), PostgreSQL, Docker, GitLab CI, Helm/Kubernetes, Vault

Internal automation platform serving 2000+ tasks/day via webhooks. Engineered reliability patterns: rate-limit priority escalation, automatic fallback on exhausted retries, Kafka-streamed metrics for observability, and access-controlled delivery filtered by Active Directory groups. Deployed to Kubernetes via GitLab CI with Vault-managed secrets and structured JSON logging. **Winner of "Best IT Project of 2025"** internal company award.

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
