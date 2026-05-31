# Interview Cheatsheet — Artem Shishkin

Файл-шпаргалка для подготовки к интервью на позиции L2/L3 Tech Support / SRE / Automation.  
Всё ниже — твои реальные цифры, кейсы и формулировки. Перечитывай перед каждым созвоном.

---

## 1. Elevator Pitch (30–60 секунд)

> I'm a Tech Support Engineer with 8 years of hands-on experience across L2/L3 support, incident management, and support automation. I've built AI-powered support systems handling 2000+ tasks per day with a 15% auto-resolution rate, and I've managed production incidents for 40+ microservices at 99.9% uptime SLA. I'm now looking to build a support function from scratch in a startup environment — applying automation and AI to make support scalable from day one.

**Короткая версия (20 сек, холодный LinkedIn-звонок):**

> I've spent 8 years bridging support and engineering — I automate support workflows, build AI agents for ticket triage, and manage incidents for high-load platforms. I'm looking for a startup where I can build the support function from zero.

---

## 2. Ключевые цифры (Numbers to Memorize)

| Что | Цифра |
|-----|-------|
| Общий опыт | **8 лет** |
| Микросервисов под наблюдением | **40+** |
| SLA (uptime) | **99.9%** |
| Задач/день через AI-платформу | **2000+** |
| Auto-resolution rate | **~15%** |
| Сэкономлено engineering hours/month | **200+ ч/мес** |
| Сэкономлено manual triage hours/month | **200+ ч/мес** |
| Внутренних инструментов построено | **5+** |
| Команд, использующих инструменты | **10+** |
| Релизная подготовка: было → стало | **20 мин → 2 мин** |
| Компании в опыте | **Home Credit (100M+ клиентов), Tinkoff (neobank-единорог)** |

---

## 3. STAR-кейсы (4 основных)

### Кейс 1: AI-платформа для саппорта (Best IT Project 2025)

- **Situation:** Ручная сортировка тикетов, долгий routing, no-code инструментов не было.
- **Task:** Построить платформу, где нетехнические сотрудники создают AI-агентов под любые типы тикетов.
- **Action:** FastAPI + LangChain + LangGraph + N8N. Слушаем Service Desk webhooks, авто-выбираем промпт из каталога, обогащаем контекст из Confluence + векторной базы + Graylog, отдаём структурированный результат. Docker, GitLab CI, Vault.
- **Result:** 2000+ задач/день, 10+ команд используют, **«Best IT Project of 2025»** внутри компании, 200+ часов/мес сэкономлено.

### Кейс 2: RAG-авторезолв тикетов

- **Situation:** Инженеры тратили часы на однотипные тикеты, root cause которых уже был известен.
- **Task:** Автоматически находить решение и закрывать тикеты без участия человека.
- **Action:** RAG-система на Python/LangChain. Парсим описание тикета + логи + скриншоты → ищем в векторной базе знаний и Graylog-логах → определяем root cause → публикуем валидированное решение.
- **Result:** **~15% авторезолв**, **200+ engineering часов/мес** сэкономлено.

### Кейс 3: Прод-инциденты для 40+ микросервисов (SRE)

- **Situation:** High-load банковская платформа, 40+ микросервисов в Kubernetes, сложная инфраструктура.
- **Task:** Держать 99.9% uptime SLA, быстро находить root cause при инцидентах.
- **Action:** L3 эскалация, on-call rotation. Log forensics через Splunk/Graylog/Kibana + SQL-запросы (Oracle, PostgreSQL) + корреляция метрик в Grafana. Проактивные дашборды и алерты. Постмортемы + runbooks.
- **Result:** **99.9% SLA достигнут и поддерживался**, снижен mean time to detection, инциденты предотвращались до user impact.

### Кейс 4: Автоматизация релизов (20 мин → 2 мин)

- **Situation:** Релизная подготовка требовала ручных проверок чеклистов и занимала ~20 минут.
- **Task:** Сократить время подготовки релиза и исключить человеческий фактор.
- **Action:** Python-валидатор: авто-проверки перед деплоем, верификация test coverage, step-by-step релизный план с rollback-инструкциями.
- **Result:** **20 мин → 2 мин**, меньше ошибок, стандартизированный процесс.

---

## 4. Техническая шпаргалка (Technical Quick Answers)

### 4.1 Linux

> **Q:** How do you debug a production issue on Linux?
> **A:** Start with `top`/`htop` for CPU/memory, `df -h` / `du -sh` for disk, `netstat -tlnp` / `ss` for ports, `journalctl -u <service> -f` for logs, `strace -p <pid>` for syscalls. For network: `curl -v`, `tcpdump`, `traceroute`. Check system limits: `ulimit -a`.

> **Q:** What's the difference between a hard link and a symlink?
> **A:** Hard link = same inode, survives original deletion, can't cross filesystems. Symlink = separate inode pointing to path, breaks if target is deleted, can cross filesystems.

> **Q:** How does `kill -9` differ from `kill -15`?
> **A:** `-15` (SIGTERM) = graceful shutdown, process can catch and clean up. `-9` (SIGKILL) = kernel kills immediately, no cleanup possible. Always try `-15` first.

### 4.2 Docker

> **Q:** What's the difference between CMD and ENTRYPOINT?
> **A:** CMD = default arguments, easily overridden at `docker run`. ENTRYPOINT = the actual executable, not overridden unless `--entrypoint` flag used. Best practice: ENTRYPOINT for the binary, CMD for default flags.

> **Q:** How do you reduce Docker image size?
> **A:** Multi-stage builds, Alpine-based images, `.dockerignore`, combine RUN layers, remove package cache (`apt-get clean`), use specific version tags (not `latest`).

> **Q:** How does Docker networking work?
> **A:** Bridge (default, isolated), Host (shares host network), Overlay (multi-host swarm), None (no networking). Containers communicate via service names in user-defined bridge networks.

### 4.3 Kubernetes

> **Q:** What happens when you run `kubectl apply -f deployment.yaml`?
> **A:** Request → API Server (auth/authz/admission) → etcd (desired state stored) → Deployment Controller creates ReplicaSet → ReplicaSet Controller creates Pods → Scheduler assigns Pods to Nodes → Kubelet on Node creates containers via CRI.

> **Q:** How do you debug a CrashLoopBackOff pod?
> **A:** `kubectl describe pod <name>` — check events. `kubectl logs <pod>` (add `--previous` for crashed container). `kubectl exec -it <pod> -- /bin/sh` if container stays alive long enough. Check resource limits, readiness probes, missing configs/secrets.

> **Q:** What's a Helm values file?
> **A:** YAML file that overrides default chart values. Used to configure different environments (dev/staging/prod) from the same chart. Managed environment-specific values for 40+ services.

> **Q:** How do you handle secrets in K8s?
> **A:** HashiCorp Vault (experience), Kubernetes Secrets (base64 — not secure by default), Sealed Secrets, External Secrets Operator. I used Vault for all 40+ services.

### 4.4 Monitoring & Observability

> **Q:** Grafana — what did you monitor?
> **A:** Custom dashboards for: service health (latency, error rate, throughput), infrastructure (CPU, memory, disk, network), business metrics. Alerts configured with thresholds, sent to on-call channels.

> **Q:** Splunk / Graylog / Kibana — how do you search effectively?
> **A:** Start with time range, narrow by service/host, search for ERROR/WARN/exception patterns. Correlate timestamps across multiple services. In Splunk: `index=* service=foo ERROR | timechart count`. In Kibana: Lucene query `level:ERROR AND service:foo`.

> **Q:** Difference between metrics, logs, and traces?
> **A:** Metrics = numerical data over time (Grafana/Prometheus). Logs = discrete events with context (Splunk/Graylog/ELK). Traces = request flow across services (Jaeger/Zipkin). Combined = observability.

### 4.5 Python & FastAPI

> **Q:** How does asyncio work?
> **A:** Single-threaded event loop. `async/await` allows cooperative concurrency — while one task awaits I/O, another runs. Good for I/O-bound work (APIs, DB queries), not CPU-bound. FastAPI is built on this.

> **Q:** What's dependency injection in FastAPI?
> **A:** `Depends()` — reusable logic for auth, DB sessions, config. Declared in function signature. FastAPI auto-resolves and injects. I use it for Keycloak/OAuth2 auth checks and DB connections.

> **Q:** How do you handle errors in FastAPI?
> **A:** Custom exception handlers (`@app.exception_handler`), `HTTPException` with status codes, Pydantic validation errors auto-return 422. Global middleware for logging unhandled errors.

### 4.6 RAG & LangChain

> **Q:** How does your RAG system work, step by step?
> **A:** 1) Ticket text + attachments → text extraction. 2) Embedding model converts to vectors. 3) Similarity search in vector DB (Confluence docs, API docs, past tickets). 4) Graylog query for recent errors matching the service/time. 5) Retrieved context + original ticket → LLM prompt. 6) LLM generates root cause + resolution. 7) If confidence high → auto-resolve. If low → suggest to agent.

> **Q:** What's the difference between LangChain and LangGraph?
> **A:** LangChain = linear chains of LLM calls. LangGraph = stateful, graph-based flows with branching, loops, and conditional routing. I use LangGraph for complex multi-step ticket resolution workflows where the agent decides next steps dynamically.

> **Q:** What embedding model / vector DB did you use?
> **A:** *(Честно ответить, что использовал — если OpenAI embeddings, то так и сказать. Если локальные, тоже. Главное — понимать концепт, а не модель.)*

### 4.7 OAuth 2.0 / Keycloak

> **Q:** How does the OAuth 2.0 Authorization Code flow work?
> **A:** 1) User → Client → Authorization Server (Keycloak), redirect to login. 2) User authenticates → Authorization Code returned. 3) Client exchanges code for Access Token + Refresh Token. 4) Access Token used for API calls. 5) Refresh Token used to get new Access Token when expired.

> **Q:** What did you use Keycloak for?
> **A:** Centralized auth for all internal tools. Integrated via FastAPI dependency injection — each endpoint checks token validity, roles, and permissions through Keycloak middleware.

### 4.8 CI/CD

> **Q:** Describe your CI/CD pipeline.
> **A:** Git push → GitLab CI triggers: 1) Lint + typecheck. 2) Tests. 3) Build Docker image. 4) Push to registry. 5) Deploy via Helm/Kubectl to K8s. Secrets via Vault Agent. Rollback = apply previous image tag. I set up this flow for all my automation services.

---

## 5. Поведенческие вопросы (Behavioral — готовые ответы)

### «Расскажи про конфликт с коллегой/разработчиком»

> В Tinkoff был случай: разработчик утверждал, что баг на стороне клиента, а не на бэкенде. Я не спорил — собрал логи с обоих сторон, воспроизвёл баг, показал trace запроса, где было видно, что бэкенд возвращает некорректный статус. Предоставил полный bug report с reproduction steps. Разработчик согласился и пофиксил в тот же день. Вывод: data beats opinions.

### «Расскажи про провал и чему ты научился»

> На старте работы SRE я один раз не проверил лимиты памяти для нового микросервиса в staging. Во время нагрузочного тестирования OOMKill убил не только его, но и соседние поды на той же ноде. Научился: всегда проверять resource limits, читать Helm values перед деплоем, настраивать алерты на OOM-события. После этого инцидента внедрил проверку лимитов в релизный пайплайн.

### «Как приоритизируешь задачи, когда всё горит?»

> Матрица: impact × urgency. P1 (prod down, user-facing) > P2 (degraded, workaround exists) > P3 (internal tooling) > P4 (improvements). Если два P1 — делаю параллельно с коллегами или эскалирую. Всегда держу stakeholder communication: «видим проблему, ETA такой-то, апдейт через 30 минут».

### «Как ты работаешь с нетехническими коллегами?»

> Мой AI-platform как раз для этого и строилась — no-code builder агентов. Я переводил запросы саппорт-команды в технические фичи, делал простые интерфейсы (N8N webhooks + шаблоны промптов), документировал понятным языком. Научился: не использовать жаргон, показывать на примерах, спрашивать «какую проблему ты пытаешься решить?», а не «какую фичу тебе сделать?».

### «Почему хочешь уйти в стартап?»

> В enterprise я построил автоматизацию на зрелой инфраструктуре. Хочу применить этот опыт в стартапе, где поддержку нужно выстраивать с нуля — выбрать инструменты, настроить процессы, заложить фундамент, который будет масштабироваться. Мне нравится ownership и видимый импакт, который даёт стартап-среда.

### «Где видишь себя через 3–5 лет?»

> Хочу вырасти в Support Engineering Lead или перейти на стык поддержки и платформенной автоматизации — строить AI-native support systems, которые решают большую часть проблем до того, как пользователь заметит.

---

## 6. Вопросы для интервьюера (Questions to Ask)

Заранее выбери 3–4, которые уместны для компании и этапа интервью.

### Про команду и процессы

- «What's the current support setup — team size, on-call rotation, escalation path?»
- «What's the balance between reactive (tickets) and proactive (automation) work expected in this role?»
- «How do support and engineering teams collaborate today? Any friction points?»
- «What's the typical incident volume and severity mix?»

### Про стек и инфраструктуру

- «What's your stack for monitoring, logging, and alerting?»
- «Do you use Kubernetes? How are secrets managed?»
- «What service desk / ticketing system do you use?»
- «Is there existing automation in the support pipeline, or is it mostly manual?»

### Про рост и культуру

- «What does success look like for this role in the first 3, 6, and 12 months?»
- «How does the company approach professional development and learning?»
- «What's the biggest challenge the support team is facing right now?»
- «How did this role open up? Is it a new position or backfill?»

### Только для стартапов

- «What's the runway and current stage of the company?»
- «What's the split between enterprise and self-serve customers in support load?»
- «Do you foresee this role growing into a team lead position as the company scales?»

---

## 7. Research-шаблон (что гуглить перед созвоном)

### За 30 минут до интервью:

- [ ] Crunchbase / LinkedIn компании: размер, раунд, инвесторы, основатели
- [ ] Продукт: что делает, кто конкуренты, pricing model
- [ ] Tech stack (LinkedIn сотрудников → раздел Skills, или их engineering blog)
- [ ] Glassdoor / Blind reviews: что говорят сотрудники о культуре
- [ ] Последние новости компании: TechCrunch, блоги, релизы
- [ ] LinkedIn интервьюера: бэкграунд, общие контакты, о чём пишет

### Во время интервью — держи в голове:

- **Показывай impact через цифры.** Не «я автоматизировал процессы», а «сократил ручную работу на 200 часов в месяц».
- **Используй STAR.** Даже если не просят явно — структура помогает.
- **Задавай встречные вопросы.** Хорошие вопросы = senior-level сигнал.
- **Если не знаешь ответ:** «I haven't worked directly with that, but here's how I'd approach it...» и покажи ход мыслей.

---

## 8. Частые технические вопросы «с подвохом»

| Вопрос | Ключевая идея ответа |
|--------|---------------------|
| «DNS не резолвится — твои действия?» | `/etc/resolv.conf` → `nslookup`/`dig` → проверить nameserver → проверить firewall → проверить, не кеш ли это → проверить upstream DNS |
| «Сервис отвечает 502 — что делаешь?» | Проверить, жив ли upstream → логи upstream-сервиса → не упирается ли в таймаут → не кончилась ли память → проверить health endpoint |
| «Pod в статусе Pending — почему?» | `kubectl describe pod` → Events: недостаточно ресурсов на нодах, PVC не привязан, node selector/taints, image pull issues |
| «Чем отличается scale-up от scale-out?» | Scale-up (vertical) = больше CPU/RAM на ноду. Scale-out (horizontal) = больше реплик. K8s encourages scale-out. |
| «Как работает garbage collection в Python?» | Reference counting + generational GC для циклических ссылок. `gc` модуль для ручного управления. Слабые ссылки (`weakref`) для кешей. |
| «Что такое connection pooling и зачем?» | Переиспользование открытых соединений к БД вместо открытия нового на каждый запрос. Экономит overhead TCP-handshake и аутентификации. Использую через SQLAlchemy/asyncpg. |

---

*Последнее обновление: май 2025. Перечитывай перед каждым интервью, особенно разделы 2, 3 и 6.*
