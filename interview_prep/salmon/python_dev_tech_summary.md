# Пояснения к python_dev_tech.md

> Краткий путеводитель по документу технической подготовки к интервью в Salmon (Senior Python Engineer — MCP Integration Layer).

Документ `python_dev_tech.md` (836 строк) создан и вычитан. Все утверждения привязаны к реальному коду `summarizer-it`.

## Что внутри

**8 блоков, всё привязано к твоему реальному коду `summarizer-it`**:

- **Блок 0 — Self-positioning.** Переформирование: твой `summarizer-it` = integration layer для агентов = та же роль, только без MCP-обёртки. Честные фрейминги про ~3 года Python (а не 5+), self-taught, AI-ассистентов.
- **Блок 1 — Глоссарий.** Идемпотентность, полиморфизм, инкапсуляция, наследование/абстракция, SOLID, DRY/KISS/YAGNI, coupling/cohesion, мутабельность, чистые функции, lazy/eager, eventual/strong consistency, optimistic locking/ETag, backpressure, concurrency-примитивы, reentrancy/race/deadlock — у каждого «где у меня в коде».
- **Блок 2 — Python internals.** GIL, event loop / coroutines / Tasks / Futures, `async/await`-механика (3 уровня), threading vs multiprocessing vs asyncio (таблица), GC (refcount + generational + `__del__`), память/референсы, декораторы, descriptors, context managers, generators, Pydantic v2, dataclass vs BaseModel, dunder-протоколы.
- **Блок 3 — FastAPI.** ASGI vs WSGI, DI (`Depends`, честная самооценка про globals), Pydantic в FastAPI, custom exception handler, `BackgroundTasks` vs `create_task`, lifespan, routing/OpenAPI/response classes, streaming/WebSockets, почему FastAPI подходит для MCP.
- **Блок 4 — System design.** REST, idempotency keys, versioning, error envelope, access-controlled RAG; retry/backoff/jitter (с указанием, что у тебя 7s fixed — improvement), circuit breaker, bulkhead, rate limiting, timeout budget; observability (logs/metrics/traces, RED/USE, SLI/SLO); contract testing (Pact); **MCP глубоко**: архитектура, lifecycle, tools/list/call JSON-RPC examples, tool annotations (новое 2025-06-18), `FastMCP` + код-скелет, **маппинг твоих клиентов в MCP tools** (killer answer); AWS/EKS/Terraform концептуально; разбор system design-question 1000 RPS.
- **Блок 5 — Заготовки про пробелы.** 8 честных ответов: 5+ лет, MCP, AWS, Terraform, contract testing, on-call, CS-образование, AI в работе.
- **Блок 6 — Банк из 40 вопросов** с готовыми ответами, каждый укоренён в твоём коде (точные `file:line` ссылки: `httpx_async.py:85-93`, `prompts_loop.py:154`, `botrate_agent.py:241`, `keycloak_client.py:77`, `single_prompt.py:81`, и т.д.). Включает код-сниппет `retry_async` с exponential+jitter (Q30).
- **Блок 7 — Вопросы интервьюеру.** 10 штук по 4 категориям.
- **Финальные советы** — 8 пунктов про честность, привязку к коду, SRE-фон как козырь, паузы и пр.

## Ключевая идея позиционирования

> «summarizer-it — это и есть integration layer для LLM-агентов: Pyrus-вебхуки → параллельный сбор контекста → LLM → постинг результата. Принципы проектирования идентичны MCP. Разница только в обёртке (без MCP) и в инфре (внутренний K8s vs EKS).»

Этой фразой ты переводишь разговор из «у меня нет MCP-опыта» в «я уже делал эту работу, просто под другим протоколом».