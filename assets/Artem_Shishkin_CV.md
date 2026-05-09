Artem Shishkin • Python Developer | Internal Tools & AI Automation

# Summary

Internal tools and AI automation engineer. I build end-to-end solutions — from simple scripts to AI agents — that eliminate manual workflows and save teams hundreds of hours per month. Stack: Python, FastAPI, LLMs/RAG, LangChain, Docker, CI/CD.

Self-driven, full-cycle ownership: I define the problem, design the solution, write the code, deploy to production, and monitor the result. Looking for a role focused on internal tooling and AI-powered automation.

# Skills

- **Languages**: Python, SQL
- **Backend**: FastAPI, asyncio, httpx, pydantic, SQLAlchemy, pytest
- **AI & LLM**: RAG, LangChain, LangGraph, OpenAI-compatible APIs, Prompt Engineering
- **Internal Tools & Automation**: N8N, workflow design, requirements gathering
- **Databases**: PostgreSQL, Redis
- **DevOps**: Linux, Docker, GitLab CI, Kubernetes, Helm, Vault
- **Observability**: Grafana, Graylog, Splunk, Kibana
- **Other**: Git, JIRA, Confluence, OAuth 2.0, Keycloak

# Experience

__Automation Engineer, Home Credit International, __Remote	Dec 2023 – Present

Home Credit International is a global consumer finance provider focused on emerging markets, with over 100 million customers across 9 countries

Solve business and IT tasks end\-to\-end: design, build, deploy, and maintain internal apps from scratch to production for multiple teams and stakeholders across the company, using both code \(Python\) and low\-code \(N8N\) approaches\.

Apps are:

- Integrated with various internal systems and services via Keycloak\-based OAuth 2\.0 authentication
- Connected to internally deployed open\-source LLMs and vector DBs \(for applying the RAG approach\)
- Include custom logging, metrics, Grafana dashboards and alerts
- Containerized in Docker and deployed via GitLab CI pipelines to VMs and K8s with Vault\-managed secrets

Each project automates processes, saving significant time for employees\. Projects described below in the "Projects" section\.

__Site Reliability Engineer, Home Credit International, __Remote	Jun 2019 – Nov 2023

- Maintained a high\-load, cross\-platform banking application consisting of 40\+ microservices running in Kubernetes \(production and test environments\)
- Installed updates and managed microservice configs, Helm values, Vault secrets, and network access rules
- Used CI/CD tools such as GitLab Pipelines and Jenkins jobs to automate deployments
- Analyzed logs and metrics using Splunk, Graylog, Kibana, and Grafana
- Built proactive monitoring \(dashboards and alerts\)
- Performed SQL queries in Oracle and PostgreSQL DB's for troubleshooting and data analysis
- Worked within Agile frameworks including Scrum, SAFe, and Kanban

__Technical Support Engineer, Tinkoff Bank, __On\-site \(Moscow, Russia\)	Jun 2017 – May 2019

Tinkoff Bank is one of the world's largest neobanks with no physical branches and a strong focus on digital services

- Provided technical support for high\-load investment services \(web and mobile apps\)
- Investigated and resolved customer issues via the Service Desk
- Escalated critical issues and product improvement suggestions to product teams
- Collaborated with developers to troubleshoot and resolve complex cases

__Projects__

- __Service Desk AI Agent__

Integrated into Service Desk and designed as a no\-code AI agent builder, enabling non\-technical users to create custom agents for any ticket form, regardless of complexity or field structure:

- Listens to task update webhooks and retrieves task data
- Selects a prompt and extra settings from a dynamic catalog based on task type
- Calls an LLM to generate structured summaries or conclusions, which are posted back into the ticketing system

Handles __2000\+ tasks per day__, regardless of their type\. __One of the winners of the internal company award "Best IT Projects of 2025"__\.

- __Automated Ticket Resolution App__
- Integrated with the Service Desk to fetch, parse, and analyze ticket descriptions, logs, and screenshots
- For non\-typical cases, finds relevant documentation about the process and used API methods in a vectorized knowledge base, searches for them in Graylog logs, detects the root cause of the user's problem and auto\-publishes a solution in the ticket
- __Solves ~15% of tickets automatically__, including the auto\-publishing of validated solutions directly into the ticket system
- __Saves an estimated 200\+ hours__ of support engineer time monthly, enabling the team to focus on complex, high\-priority incidents
- __Jira Task Validator__

Retrieves a Jira task for installing a release update and checks whether it is ready to be deployed\. 

It performs the following validations:

- Verifies that the current production build image exists in the registry \(to allow rollback if needed\)
- Checks that the new build image specified in the task exists in the registry
- Confirms that the new build version has been fully tested on the required test environments

Then, it generates a dynamic step\-by\-step release plan, which includes:

- Steps to prepare before the release
- Steps to deploy the new version
- A list of useful resources to check right after the new version is deployed \(e\.g\., links to logs, dashboards\)
- Rollback instructions in case something goes wrong

This tool __reduced the release preparation time__ from over 20 minutes to just a few minutes per task\.

- __Service Desk Reporting Tool__

Improves visibility into support team performance and provides clear insights into ticket classifications:

- Aggregates ticket data in real time and stores it in a database
- Generates daily, weekly, and monthly reports with CSV exports and pie chart visualizations
- Automatically sends reports to stakeholders via corporate messenger and email groups

In addition, the exported reports are analyzed by an LLM, which generates summary and suggestions for improvement and highlights the most problematic areas in the services supported by the team

- __Apps Stores Ratings & Reviews__
- Collects and analyzes ratings & reviews from multiple stores \(App Store, Galaxy Store, App Gallery, etc\.\) for multiple company apps
- Generates metrics for Grafana dashboards
- Sends automated alerts to stakeholders when app ratings begin to decline

# Certificates

- n8n Courses \(Level 1 [CERTIFICATE](https://community.n8n.io/badges/104/completed-n8n-course-level-1?username=shishkin), Level 2 [CERTIFICATE](https://community.n8n.io/badges/105/completed-n8n-course-level-2?username=shishkin)\)	December 2025
- Back End Development and APIs \(freeCodeCamp\) | [CERTIFICATE](https://www.freecodecamp.org/certification/shishkin/back-end-development-and-apis)	July 2023
- JavaScript Algorithms and Data Structures \(freeCodeCamp\) | [CERTIFICATE](https://www.freecodecamp.org/certification/shishkin/javascript-algorithms-and-data-structures)	February 2023

# Education

Specialist, Marketing — Russian State Social University (2012)
