# Artem Shishkin
**Site Reliability Engineer**

[LinkedIn](https://linkedin.com/in/ashishkin21) | [Telegram](https://t.me/ashishkin21) | ashishkin21@gmail.com | Israel, Center District

---

## Summary

Site Reliability Engineer — 99.9% SLA on a 40+ microservice banking platform in Kubernetes, with on-call, SLI/SLO, error budgets, and RCA/postmortem discipline.
Stack: Kubernetes/Helm, GitLab CI/CD, Prometheus/VictoriaMetrics, Grafana, ELK, Kafka, PostgreSQL, Oracle, Redis — scripted in Python.
Bringing build-it-run-it ownership from requirements to production support to an Antifraud/AML/KYC platform operating at real-time scale.

---

## Skills

**Infrastructure & Orchestration:** Kubernetes, Helm, Docker, Linux, HashiCorp Vault, Network Policies, Ingress, RBAC, Load Balancing, Fault Tolerance  
**Observability:** Prometheus, VictoriaMetrics, Grafana, ELK (Kibana), Splunk, Graylog, RED/USE, Four Golden Signals, Structured JSON Logging  
**SRE Practices:** SLI/SLO, Error Budgets, On-Call, Incident Response, RCA / Postmortem, Runbooks, Capacity Planning  
**CI/CD & Scripting:** GitLab Pipelines (templates, secrets handling), Helm Charts, Jenkins, Python  
**Data:** PostgreSQL, Oracle, Redis, Kafka, SQL  
**Security:** OAuth 2.0, Keycloak, JWT/JWKS (RS256)  
**Methodology & Tools:** Git, JIRA, Confluence, Agile, Scrum, SAFe, Kanban  

---

## Experience

### Automation Engineer — Home Credit International
**Remote | December 2023 – Present**

*Home Credit International — global consumer finance provider with 100M+ customers across 9 countries*

- Owned 5+ internal platform services end-to-end — from requirements gathering with stakeholders through deployment, production operation, and user-facing incident support — eliminating **200+ hours/month** of manual work across 10+ teams
- Containerized services with Docker and deployed to VMs and Kubernetes via GitLab CI/CD pipelines, with HashiCorp Vault-managed secrets and structured JSON logging
- Built an internal automation platform handling 2000+ tasks/day via webhooks — engineered resilience with rate-limit priority escalation and automatic fallback on exhausted retries, and streamed service metrics to Kafka for observability and incident triage
- Configured Grafana dashboards and alerts for service health and latency, and secured APIs with Keycloak JWKS/RS256 token verification
- Won **"Best IT Project of 2025"** company award for a no-code internal platform adopted across 10+ teams

### Site Reliability Engineer — Home Credit International
**On-site | Moscow, Russia | June 2019 – November 2023**

- Maintained **99.9% uptime SLA** for a high-load banking platform of 40+ microservices in Kubernetes — operated a multi-component architecture with load balancing and fault-tolerance across production and test environments
- Defined and tracked **SLI/SLO** with **error budgets**; participated in **on-call rotation (24/7)** for incident response, escalation, and service restoration
- Conducted **root cause analysis** and **postmortems** for production incidents — correlated metrics, logs, and traces, and ran SQL queries against Oracle and PostgreSQL to localize failures and resolve them
- Built proactive monitoring dashboards and alerts using **Prometheus / VictoriaMetrics**, Grafana, Splunk, Graylog, and Kibana — applied **RED/USE** and the **Four Golden Signals** to surface latency, errors, saturation, and traffic before user impact
- Wrote and maintained **Helm values** and charts, **Vault secrets**, and **network access rules** for 40+ services; managed ingress, RBAC, and service-to-service policies
- Automated deployment workflows via **GitLab Pipelines** and Jenkins — introduced pipeline templates and secrets injection, reducing deployment time and manual errors
- Authored **runbooks** and **technical documentation** for operational procedures, incident playbooks, and service onboarding
- Addressed infrastructure issues across compute, network, and configuration; eliminated recurring product failures through code, config, and process fixes

### Technical Support Engineer — Tinkoff Bank
**On-site | Moscow, Russia | June 2017 – May 2019**

*Tinkoff Bank — one of the world's largest neobanks with no physical branches, fully digital-first*

- Provided technical support for high-load investment services (web and mobile apps), investigating and resolving customer issues via Service Desk while maintaining resolution SLA and customer satisfaction
- Triaged incidents, collected and analyzed logs, reproduced bugs, and escalated critical cases to L3 and development teams with thorough diagnostic summaries
- Bridged frontend and backend systems to troubleshoot complex technical cases across the full stack — foundation for the move into site reliability engineering

---

## Projects

### Internal Automation Platform
**Stack:** Python, FastAPI, Kafka, Keycloak (JWKS), PostgreSQL, Docker, GitLab CI, Helm/Kubernetes

Internal automation platform serving 2000+ tasks/day via webhooks. Engineered reliability patterns: rate-limit priority escalation, automatic fallback on exhausted retries, Kafka-streamed metrics for observability, and access-controlled knowledge delivery filtered by Active Directory groups. Deployed to Kubernetes via GitLab CI with Vault-managed secrets and structured JSON logging. **Winner of "Best IT Project of 2025"** internal company award.

### Jira Task Validator (Deployment Readiness)
**Stack:** Python, FastAPI, Docker Registry API, Jira API

Retrieves Jira release tasks and validates deployment readiness across 3 checks: current production image exists in registry (rollback safety), new build image exists, and test environment coverage is complete. Generates a dynamic step-by-step release plan including pre-release steps, deployment steps, post-deploy verification resources, and rollback instructions. **Reduced release preparation time from 20+ minutes to under 2 minutes per task.**

### Service Metrics Aggregation & Reporting
**Stack:** Python, PostgreSQL

Aggregates ticket and service metrics in real time into PostgreSQL, and generates daily/weekly/monthly reports with CSV exports and pie-chart visualizations. Auto-delivers reports to stakeholders via corporate messenger and email; highlights problematic service areas for capacity and reliability planning.

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