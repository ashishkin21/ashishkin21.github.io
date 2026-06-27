# Техническая подготовка — Salmon, Senior Python Engineer (MCP Integration Layer)

> Конспект + Q&A. Привязан к реальному коду `summarizer-it`. Цель — на интервью каждое утверждение подтверждать ссылкой на собственный проект, опираться на него.
> Использовать вместе с `python_dev_hr.md` (HR-раунд).

---

## Как пользоваться этим документом

- Блоки 0–4 — это «конспект на повторение в ночь перед». Каждый термин/концепт: короткое определение + «где это у меня в коде».
- Блок 5 — заготовки ответов на вопросы о пробелах (без вранья).
- Блок 6 — банк вопросов. Прорепетируй вслух хотя бы 10–12 из них, остальные просмотри.
- Блок 7 — вопросы, которые ты задаёшь интервьюеру. Выбери 3–4.

---

# Блок 0. Самооценка и self-positioning (важнее всего)

## Ключевое переформирование роли

Вакансия: «integration layer, через который LLM-агенты вызывают внутренние API компании».
Мой `summarizer-it` **— это и есть integration layer для агентов**. Только:
- вместо MCP-контракта — вебхук Pyrus + REST `/botrate`;
- вместо вызова «tool by name» — lookup промпта в реестре Pyrus (`find_multiprompts`);
- вместо tools.list/tools.call — динамический каталог промптов с шагами и `order`;
- клиенты к 11+ внутренним сервисам (Pyrus, Confluence, KHub, Minerva, Graylog, N8N, Kafka, Keycloak, Vault, LDAP, LLM-Integration) — это буквально «tools».

То есть ты **уже делал работу, описанную в вакансии**. Разница — в обёртке (MCP vs свой протокол) и в инфре (внутренний K8s vs EKS). Это — точка опоры.

## Честный фрейминг про «5+ лет и senior»

| Вопрос в голове | Честный переформулированный ответ |
|---|---|
| «У меня ~3 года на Python, не 5+» | «8 лет в технических ролях. Python — основной язык последние 3 года после перехода из SRE в разработку. До этого 4+ года эксплуатация железобетонной banking-платформы с 40+ микросервисами — это научило писать именно тот код, который не падает в продакшене и который можно дежурить. Так что по совокупности — практический senior-опыт есть, хоть формальный Python-стаж меньше». |
| «Я self-taught, нет CS-образования» | «Я самоучка, у меня нет CS-диплома. Но я закрываю теорию по мере нужды и сразу применяю — 5+ сервисов в продакшене, обслуживающих 2000+ задач/день, говорят, что практический результат есть. Я честно знаю, где у меня пробелы, и компенсирую их целенаправленно». |
| «Я консультируюсь с AI при принятии решений» | (На некоторых интервью это минус, на некоторых — плюс. Прозрачно: «Пользуюсь AI как accelerated-ревьюером и brainstorm-партнёром; финальные решения и ответственность — мои. Это ускорение моей производительности, а не костыль».) |

## Главная мантра ответа на «расскажи о себе»

> 3 предложения:
> 1. «Python-разработчик, последние 3 года строю AI-автоматизацию в Home Credit International; до этого 4 года SRE на платформе с 40+ микросервисами».
> 2. «Мой флагман — `summarizer-it`, integration layer для LLM-агентов: Pyrus-вебхуки → параллельный сбор контекста из Confluence/KHub/Graylog → LLM → постинг результата обратно. По сути это та же роль, что и у вас, только без MCP-обёртки.»
> 3. «4+ года SRE дали мне именно production-мышление — я не просто пишу, я дежурил код, который написал: retry, circuit breaker, structured logging, метрики, идемпотентность, read-only fs в K8s. Это база, на которой role-specific-знания надстраиваются быстро.»

---

# Блок 1. Фундаментальная терминология (глоссарий)

Каждый термин: короткое определение + где встречается в `summarizer-it`. Если на интервью назвали термин — отвечай **определение + пример из своего кода**.

### Идемпотентность (idempotency)
Вызов `f(x)` можно повторять сколько угодно — результат и состояние системы те же, что от одного вызова.
- У меня: дедуп вебхуков через `tasks_queue` (`app.py:595`), чтобы один и тот же Pyrus-хук не отработал дважды; `pyrus_client.update_task` с `field_updates` — установка значения поля, при повторе значение то же (`single_prompt.py`, `prompts_loop.py:97`); `executed_prompts`-счётчик в `prompts_loop.py:154` — один промпт не выполнится больше `max_executions_per_prompt`.
- В tool-API для агентов: критично, потому что **агенты ретраят**. Любой tool с side effects должен принимать idempotency-key: второй вызов с тем же ключом — no-op или возврат того же результата.

### Полиморфизм (polymorphism)
Один интерфейс — много реализаций.
- У меня: `AsyncHTTPClient` (`utils/httpx_async.py:12`) — базовый класс с `request/get/post/put/delete`. Под ним: `LLMIntegration`, `KeycloakClient`, `N8NClient`, `JayKHubClient` — каждый переопределяет только нужное, но `.post(...)` работает одинаково. Диспетчеризация — через late binding на `__class__`. Это **subtype-полиморфизм** (Pythonic duck typing + наследование).
- See also: dunder-методы (`__aenter__/__aexit__`, `__del__`) — это *ad-hoc* (operator) полиморфизм.

### Инкапсуляция (encapsulation)
Скрытие внутреннего состояния; доступ через контракт.
- У меня: `KafkaClient._get_producer()` (`kafka_client.py:18`) — ленивая инициализация приватного `self._producer`. Внешний код зовёт `send_botrate_metric()` и не знает про внутреннее управление коннектом. `_jwks_url` / `_last_known_kid` в `KeycloakClient` — приватные; снаружи только `verify_token()`.

### Наследование / абстракция
- У меня: `KeycloakClient(AsyncHTTPClient)`, `LLMIntegration(AsyncHTTPClient)`, `N8NClient(AsyncHTTPClient)` — все наследуют retry-логику базового `request()`. Это **re-use через generalization** (базовый класс = общий контракт). Минус, который я понимаю: mixin/композиция часто чище, и у меня base-class перегружен URL-специфичной логикой под LLM/Pyrus/VK Teams — это запах «божественного базового класса». (Честная самооценка на интервью.)

### Абстракция (abstraction)
Выделение существенных характеристик, скрытие несущественных.
- У меня: `wrapper()` (`utils/wrapper.py:10`) абстрагирует «вызови async-функцию и обработай ошибки осмысленно» — всем 11+ клиентам не нужно дублировать try/except.
- `process_selected_prompt()` (`single_prompt.py:81`) абстрагирует весь pipeline prompt-execution; `handle_webhook()` не знает деталей сбора контекста.

### SOLID (одной фразой каждый)
- **S** — Single Responsibility: `find_multiprompts` только ищет, `process_selected_prompt` только выполняет, `_notify_user_error` только уведомляет об ошибке.
- **O** — Open/Closed: новый «tool» (= новый клиент) добавляется через новый класс `XxxClient(AsyncHTTPClient)` без правок базового `request()`.
- **L** — Liskov: подстановка наследника (`LLMIntegration`) вместо base работает — все переопределённые методы сохраняют контракт `AsyncHTTPClient.post`.
- **I** — Interface Segregation: клиенты импортируют только то, что нужно (`from utils.wrapper import wrapper`).
- **D** — Dependency Inversion: `process_selected_prompt` принимает `pyrus_client`, `llm_integration`, `keycloak_client` как параметры (`single_prompt.py:81-97`) — depends on abstraction, не создаёт сам. Это и есть **dependency injection**.

### DRY / KISS / YAGNI
- DRY: `wrapper()` — единая обработка ошибок; `AsyncHTTPClient.request` — единая retry-логика.
- KISS: stateless-функции в `functions/` (`find_multiprompts`, `filter_khub_docs_by_access`) — чистые, легко тестировать.
- YAGNI: `prompts_loop`-логика включается флагом `config.agents.prompts_loop.enabled` — не навязывается, если не нужно. (Контрпример — у меня `prisma_agent` существует, но по умолчанию `enabled: false`, это иногда YAGNI-нарушение, и я это знаю.)

### Coupling / Cohesion
- **Coupling** (связанность модулей): `handle_webhook` сильно coupled с global state (`llm_integration`, `keycloak_client`, `n8n_client`, `tasks_queue`) — это слабое место, я это знаю, и оно появилось из-за Keycloak token-refresh pattern (нужно пересмотреть управление глобальными клиентами, возможно к DI-container).
- **Cohesion** (внутренняя сцепленность): `functions/`-модули — high cohesion (один модуль = одна операция); `app.py` (1181 строк!) — low cohesion, это legacy god-module, часть логики вынес в `workflows/`.

### Мутабельность / Immutability
- Mutable: `list`, `dict`, `set`. Immutable: `tuple`, `str`, `frozenset`, `int`.
- У меня: `executed_prompts = {}` — mutable, меняется в цикле (`prompts_loop.py:124,242`). `Annotated[list, operator.add]` в `PrismaAgentState.file_ids` (`prisma_agent.py:66`) — LangGraph-редюсер работает как «immutable accumulator» (каждый узел возвращает новый кусочек, склеивается).
- Опасность: дефолтные mutables в аргументах `def f(x=[])` — классическая ловушка, у меня её нет (использую `field(default_factory=dict)` в `@dataclass`, `single_prompt.py:63`).

### Побочные эффекты / чистые функции (side effects / pure functions)
- Чистая функция: вывод зависит только от входа, не меняет внешнее состояние. `find_multiprompts(pyrus_event, tasks_registry, ...)` (~pure, aside from logging).
- Side effect: `process_selected_prompt` — пишет в Pyrus, шлёт email, логирует в Kafka. Не чистая, и не должна быть — у неё работа именно side effects.
- Принцип: отделять pure от effectful. У меня `functions/` (pure-ish) vs `tools/`+`clients/` (effectful) — это осмысленное архитектурное разделение.

### Lazy / Eager
- Lazy: `_get_kafka_client()` (`botrate_agent.py:34`) — Kafka-продюсер создаётся при первом использовании, не при старте. JWT signing key cached в `PyJWKClient` (lifespan=3600). Lazy import `from agents.botrate_agent import run_botrate_agent` внутри `botrate_endpoint` (`app.py:1071`) — избегает circular imports.
- Eager: `config = yaml.safe_load(...)` на module-load (`app.py:60`) — eager, что и есть узкое место («правки требуют рестарта»).

### Eventually consistent / Strong consistency
- Eventually consistent: Kafka-метрики (могут пройти секунды до агрегации downstream). `result.pyrus_event` может lagать от реального состояния Pyrus (поэтому есть fallback `get_task_info`).
- Strong consistency: `pyrus_client.update_task` — upstream Pyrus даёт strong consistency на стороне задачи.

### Optimistic locking / ETag / Idempotency keys
- Optimistic concurrency control: клиент держит «версию» (ETag/If-Match или version-поле), пишет — сервер отвергает, если кто-то успел обновить.
- У меня явного нет, но я понимаю: при параллельных вебхуках на одну Pyrus-задачу условие гонки возможно — `tasks_queue` + `await asyncio.sleep(2.5)` (`app.py:594`) это **poor man's lock**, не настоящий optimistic locking. Правильнее — idempotency-key по `task_id` + `nonce` и серверный дедуп.
- **Это вопрос, который тебе скорее всего зададут — как ты обеспечишь идемпотентность в tool-API для агентов.** Ответ ниже в банке вопросов.

### Backpressure
- Когда downstream медленнее upstream — нужно **сигнализировать**, что нагрузка копится. Способы: queue (`asyncio.Queue` с maxsize), rejection, self-regulating (Token bucket).
- У меня: `tasks_queue` не bounded — это и есть backpressure-проблема (при burst вебхуков все пойдут в обработку, нет reject/queue). Честная самооценка. Решение на интервью: bounded `asyncio.Queue` + worker pool, или reject 429, когда очередь полна.
- LLM-Integration 429-handling (`httpx_async.py:85-93`) — это **upstream backpressure**: service говорит «медленнее», мы уважаем, повышаем приоритет или откат на другую модель.

### Concurrency primitives recap
- `asyncio.Lock` — coarse mutual exclusion в async (atomic-секции).
- `asyncio.Semaphore` — ограничить число параллельных операций (rate limiter). **У меня не используется — пробел:** при burst параллельных вебхуков может переходить лимиты LLM-Integration. Указать как improvement.
- `asyncio.Event` — сигнал «один-ко-многим».
- `asyncio.Queue` — FIFO, bounded — для producer/consumer pattern.
- `asyncio.create_task` vs `BackgroundTasks`: см. Блок 3.

### Other terms which will pop up
- **Reentrancy**: функция реентерантна, если безопасно вызываться повторно до завершения предыдущего вызова. `wrapper()` реентерантна (pure-ish except logging). `handle_webhook` — нет (shared `tasks_queue`).
- **Race condition**: классическая опасность — проверка/действие неатомарны. `if task_id in tasks_queue: return; tasks_queue.append(...)` (`app.py:595-599`) — держится на `await asyncio.sleep(2.5)` *и на однопоточности event loop*, это не гонко-безопасно при множестве воркеров (uvicorn --workers>1).
- **Deadlock**: ни у кого явно нет (нет взаимных lock-ordering), но `await` внутри критической секции мог бы создать.
- **Throughput / Latency / Saturation** (USE/RED metrics): observability-vocab — см. Блок 4.
- **Idempotency vs commutativity**: коммутативность — порядок не важен; идемпотентность — повтор не важен.

---

# Блок 2. Python internals (под senior)

## 2.1 GIL (Global Interpreter Lock)

**Определение:** CPython-артефакт — один мьютекс на интерпретатор. В любой момент **ровно один** Python-тред исполняет Python bytecode.

- GIL удерживается тредом **между байткод-инструкциями** и освобождается периодически (каждые `sys.setswitchinterval`, default 5ms) и при I/O (sleep, read, recv).
- **Следствие:** threading **не ускоряет CPU-bound** Python-код на одном ядре. Ускоряет только I/O-bound. **Для CPU-bound — `multiprocessing`** (отдельные интерпретаторы, свой GIL у каждого).
- **PEP 703 / no-GIL** — экспериментальный free-threaded build в 3.13t/3.14t, не дефолт ещё; об этом знают, но не требовательны к деталям.

**Как рассказать про себя:** «asyncio — однопоточный, GIL не pinch point, потому что весь мой код I/O-bound. Threading я бы использовал для sync-библиотек (LDAP, Vault) — и у меня именно для этого `convert_to_async` через `asyncio.to_thread`, что под капотом пул тредов. `multiprocessing` — для CPU-bound задач вроде парсинга больших документов или ML-inference; в моём проекте CPU-bound почти нет, весь pipeline — это I/O (LLM, HTTP, SQL).»

## 2.2 Event Loop, coroutines, Tasks, Futures — точно

- **Coroutine** (`async def f()`) — функция, **которая возвращает coroutine object** при вызове. **Не запускается** сама. Запускается только `await`-ом или `loop.create_task()`/`asyncio.run()`.
- **Future** — low-level «обещание результата»: объект с состоянием pending/finished/result/exception.
- **Task** — Future, который забран планировщиком запустить coroutine как единицу работы. `asyncio.create_task(coro)` — планирует немедленно; возвращает Task.
- **`await x`** делает: если `x` — coroutine/Task/Future, приостановить текущую coroutine до результата, передать контекст в loop; loop в это время может крутить другие Tasks.
- **`asyncio.gather(*coros)`** создаёт Task для каждого и ждёт результаты списком. По умолчанию **fail-fast**: первая ошибка → проброс из gather; остальные Tasks **остаются живы**, если их не отменят. `gather(*..., return_exceptions=True)` — все exceptions возвращаются как значения.
- **`asyncio.wait(coros)`** — низкоуровневее; возвращает `(done, pending)`; не отменяет pending автоматически.
- **Контекст event loop** — `asyncio.get_event_loop()` deprecated в 3.12+, используй `asyncio.run` и `asyncio.get_running_loop()`.

**У меня в коде — конкретные проявления:**
- `asyncio.create_task(repeat_every_minute_job())` в `lifespan` (`app.py:67`) — фоновый монитор LLM-лимитов.
- `await asyncio.sleep(2.5)` в `handle_webhook` (`app.py:594`) — yield в loop.
- LangGraph `Send`-API в `botrate_agent.py:322` — fan-out к `khub_worker` параллельно, результаты аккумулируются редюсером `operator.add` в `khub_results: Annotated[list, operator.add]` (`botrate_agent.py:241`). Это **structured concurrency** поверх LangGraph, под капотом — `asyncio.gather` по Send-ам.
- Prisma-агент аналогично: `return [Send("fetch_external", src) for src in sources]` (`prisma_agent.py:270`).

## 2.3 `async/await` механика — уровни понимания

1. **Поверхностно:** «`async` делает функцию корутиной, `await` — ждёт».
2. **Senior:** `async def` создаёт объект coroutine через `types.coroutine`/generator-based механизм. Под капотом — **state machine** через `yield from`/`SEND`. `await x` эквивалентен `yield from x.__await__()`. Текущая coroutine suspends; loop resumes другие.
3. **Что важно:** `await` **БЛОКИРУЕТ ТОЛЬКО ТЕКУЩУЮ КОРУТИНУ**, не поток. Loop может крутить тысячи корутин в одном треде. Мистейк junior — вызвать `requests.get(...)` внутри `async def` без `to_thread` — заблокирует loop.

**У меня** `convert_to_async` (`utils/convert_to_async.py:6`) с `asyncio.to_thread` — корректная обёртка sync-библиотек (LDAP, Vault, Confluence API через `requests`). `to_thread` запускает sync-функцию в тредовом пуле (`concurrent.futures.ThreadPoolExecutor`) и корректно возвращает результат.

## 2.4 Threading vs Multiprocessing vs asyncio — таблица «когда что»

| Парадигма | Когда | У меня проявление |
|---|---|---|
| **asyncio** | I/O-bound, ожидаем много внешних ответов, низкий CPU. Один тред = тысячи корутин. | Весь мой проект — асинхронный (`httpx.AsyncClient`, `aiokafka`, `AsyncHTTPClient`). |
| **threading** | Блокирующий I/O в sync-библиотеках без async-native (LDAP `python-ldap`, `pyjwt` heavy crypto). GIL не мешает, т.к. треды спят на I/O. | `asyncio.to_thread`-обёртка `convert_to_async` для `python-ldap`, `hvac` (Vault). |
| **multiprocessing** | CPU-bound (number-crunching, ML-inference на CPU, парсинг больших docs). Отдельные интерпретаторы = свой GIL. IPC overhead. | Не использую — у меня нет CPU-heavy кода. Знаю, что применил бы для тяжёлых embedding computation, если бы они не были за HTTP. |
| **concurrent.futures** | Унификация API. `ThreadPoolExecutor`, `ProcessPoolExecutor`. `to_thread` использует `ThreadPoolExecutor` дефолтный (min(32, cpu+4)). | `asyncio.to_thread` под капотом. |

**Ловушка**: `asyncio` **не даёт параллелизма внутри одного треда**, только **конкурентность** (concurrency). Если две HTTP-ноги запускаются через `await` обе сразу, запросы летят конкурентно (оба клиента ждут), но байткод исполняется поочерёдно. Практически всегда это то, что нужно.

## 2.5 Garbage Collection в CPython

**3 механизма:**

1. **Reference counting (primary):** каждый PyObject имеет `ob_refcnt`. Он инкрементится при присваивании, декрементится при выходе из scope. Достиг 0 → немедленно освобождается. **Поэтому ссылка освобождается детерминированно** (в отличие от Java).
2. **Generational GC (for cycles):** refcount-циклы (A→B→A) не может разорвать. Циклический GC в 3 поколения: молодые объекты (gen 0) сканируются чаще, пережившие сканирование переходят в gen 1, и т.д. `gc.collect()` — принудительно. `gc.disable()` — disable (но refcount всё равно работает).
3. **`__del__` finalizer:** проблемный — может быть отложен или не выполниться, и (до PEP 442 в 3.4) запрещал cyclic GC собирать объект. PEP 442 починил сбор циклов с `__del__`.

**У меня** `AsyncHTTPClient.__del__` (`httpx_async.py`) — логирует деструктор. Это **характерный code smell**, потому что `__del__` не детерминирован и может срабатывать во время shutdown, когда `logger` уже сломан. Лучше — явный `close()` через `async with`. (Честная самооценка на интервью.)

**Heads-up про weakref / `__del__` + exceptions:** finalizer во время exception suppression, finalizer, который поднимает exception — теряется. Избегать.

## 2.6 Memory / References в Python

- Все объекты — heap-allocated. Variables — labels (references), не boxes. `a = []`, `b = a` — оба смотрят на один список.
- **`is` vs `==`:** `is` — identity (один ли объект в памяти), через `id()`. `==` — `__eq__`. `a == b` может быть True, когда `a is b` False.
- **Interning:** small ints (−5..256), короткие strings — интернированы (`sys.intern` явно). На этом ловят «а почему `a is b` для двух `"hello"`».
- `copy.copy` (shallow) vs `copy.deepcopy` (recursive). Mutable nested — shallow copies share children.

## 2.7 Senior-бытовое Python

### Декораторы
`@decorator` эквивалентен `f = decorator(f)`. Декоратор — callable, который принимает функцию и возвращает (обычно) функцию. **`functools.wraps`** обязателен — иначе `__name__`, `__doc__` потеряются.

### Descriptors
Объект с `__get__` (и `__set__`/`__delete__`). Properties, classmethods, staticmethods реализованы через descriptors. Pydantic v2 validators строятся через descriptor protocol.

### Context managers
- `with` синхронный — `__enter__/__exit__`.
- `async with` — `__aenter__/__aexit__`.
- У меня: `async with JayKHubClient(...)` (`botrate_agent.py:371`) — асинхронный context manager, корректно открывает/закрывает HTTP client.
- `contextlib.asynccontextmanager` для создания CM из генератора.
- `ExitStack` — динамическое управление набором контекстов.

### Generators / `yield`
- `yield` приостанавливает функцию, возвращает Generator. `next(g)` resumes. `yield from` делегирует в под-генератор.
- Use cases: streams, lazy sequences. У меня прямых генераторов нет, но понимаю механику.
- `StopIteration` + `asyncio` имеет особенность (`convert_to_async.py:71` — комментарий «StopIteration interacts badly with generators and cannot be raised into a Future»).

### Pydantic v2 (важно для FastAPI)
- Pydantic v2 — Rust core; v1-совместимый API через `pydantic.v1`. Быстрее в 5-50x.
- `model_dump()` заменил `.dict()` (deprecated). `model_dump(mode='json')` — сериализация в JSON-native типы (datetime → ISO string и т.д.) — у меня `app.py:1098`.
- `model_validate()` заменил `.parse_obj()`. `model_config` (`ConfigDict`) заменил внутренний `class Config`.
- Validators: `@field_validator` (per-field), `@model_validator` (whole-model). v1: `@validator`.
- `Annotated[int, Field(gt=0)]` — modern style.
- У меня: `BotRateRequest`, `BotRateResponse`, `KHubResult` (`models/botrate.py`) — все BaseModel; Enum через `str, Enum` для JSON-сериализации (`BotRateStatus`, `SolutionSource`).

### `dataclass` vs `BaseModel`
- `@dataclass` — stdlib, lightweight, без валидации. У меня `PromptWorkflowResult` (`single_prompt.py:54`) — `@dataclass` с `field(default_factory=dict)`.
- `BaseModel` (Pydantic) — с валидацией, JSON-schema, авто-conversion. Использую на API-границе.

### dunder-протоколы на пальцах
- `__init__` (constructor), `__new__` (allocator), `__del__` (finalizer), `__repr__`, `__eq__`, `__hash__` (mutables default `__hash__=None` — нельзя в set/dict key).
- `__aenter__/__aexit__` (async CM), `__aiter__/__anext__` (async iteration), `__await__` (make awaitable).
- `__class_getitem__` — поддержка синтаксиса `List[int]`.

---

# Блок 3. FastAPI internals

## 3.1 ASGI vs WSGI

- **WSGI** — sync протокол (PEP 3333). Reference: Flask, Django (classic). One request = one thread. Не масштабируется на long-polling/websockets без дополнительных workers.
- **ASGI** — async successor (spec by Django Channels team). Event-driven; one event loop handles thousands of connections. WebSocket support built-in.
- **FastAPI** — ASGI-фреймворк поверх Starlette (ASGI toolkit) + Pydantic. **Starlette** handles routing, middleware, requests/responses; **FastAPI** добавляет DI, OpenAPI-генерацию, type-aware validation.

## 3.2 Dependency Injection (Depends)

- FastAPI автоматически инжектит параметры-зависимости, резолвит их рекурсивно, кэширует per-request (по умолчанию `use_cache=True`).
- `Security(http_bearer)` (`app.py:1059`, `dependencies=[Security(http_bearer)]`) — security-scoped Depends. `Security` = `Depends` + scope.
- Sub-dependencies cached within single request → cheap reuse.
- Yield-dependency (генератор) — setup/teardown pattern (аналог `async with`).

**У меня слабое** — почти всё через module-level globals (`llm_integration`, `keycloak_client`) вместо `Depends`. **Если спросят про DI** — честно: «большая часть клиентов глобальные, я понимаю, что лучше через Depends + yield-dependency, особенно для тестов и Keycloak token-refresh, и это первый item рефакторинга». Это серьёзная самооценка — интервьюер оценит.

## 3.3 Pydantic в FastAPI

- Аннотации типов в сигнатуре → FastAPI валидирует request body, params, headers через Pydantic; при ошибке → 422 (`RequestValidationError`).
- `@app.post("/botrate", response_model=BotRateResponse)` (`app.py:1059`) — auto-validates и фильтрует outgoing response через `response_model`. Только поля из модели выйдут наружу.
- Генерируется OpenAPI (`/openapi.json`) и Swagger (`/docs`) автоматически.

## 3.4 Custom exception handler

- `@app.add_exception_handler(RequestValidationError, ...)` — глобальный перехват. У меня `botrate_validation_exception_handler` (`app.py:80`) — для `/botrate` возвращает кастомный `BotRateResponse` с `VALIDATION_ERROR` вместо дефолтного 422.
- Альтернатива: custom middleware (`@app.middleware('http')`) — оборачивает ВСЕ запросы, отдаёт управление через `await call_next(request)`. Middleware — для cross-cutting (корреляц-ID, timing, CORS). Exception handler — для предсказуемых error-response-shapes.

**Senior-нюанс:** middleware не видит `RequestValidationError` после того, как он поднялся, потому что FastAPI/Starlette его ловит в ExceptionMiddleware. Exception handlers — proper way.

## 3.5 `BackgroundTasks` vs `asyncio.create_task`

- `BackgroundTasks` — Starlette feature: task запускается **после** отправки response, в том же event loop. Документация гарантирует, что ответ отошёл первым. Но **если task долгая или тяжелая**, блокирует event loop (один worker). Минус: при crash mid-task состояние теряется.
- `asyncio.create_task(coro)` — запуск немедленно, не связан с request/response lifecycle. Подходит для background jobs от `lifespan` (`app.py:67`).

**У меня оба**:
- `background_tasks.add_task(handle_webhook, pyrus_event)` (`app.py:1044`) — отвечаем Pyrusу `{"data_received":"ok"}` немедленно, обработка в фоне.
- `asyncio.create_task(repeat_every_minute_job())` (`app.py:67`) — фоновая life-long job через `lifespan`.

**Trade-off, который сознаю:** `BackgroundTasks` — in-memory, single-process. При multiple uvicorn/gunicorn workers — задача в одном worker, не дублируется (хорошо), но при рестарте теряется. **Для production-critical-задач — external queue (Celery/RQ/RabbitMQ) или Kafka**. У меня Pyrus-вебхук re-delivery + `tasks_queue` компенсирует потерю, но это не durability.

## 3.6 Lifespan (startup/shutdown)

- Старый `@app.on_event("startup")` deprecated в FastAPI 0.93+. Новый — `lifespan` context manager.
- У меня `lifespan` (`app.py:62-76`) — async context manager с `yield`. До `yield` = startup, после = shutdown.
- Запуск фонового job (`create_task`), shutdown — `job_task.cancel()` + clean-up Kafka (await `job_task` для проброса `CancelledError` — правильно!).
- Альтернатива: `@asynccontextmanager` decorator (то же).

## 3.7 Routing, OpenAPI, response classes

- Path- и query-params через аннотации + `Path(...)`, `Query(...)`.
- **`NonASCIIJSONResponse`** (`app.py:17`) — мой custom response class, override `render()` для `ensure_ascii=False`. Подаётся как `default_response_class=NonASCIIJSONResponse` в `FastAPI(...)`. Ради корректного отображения русского в JSON. Senior-нюанс: при этом заголовки и content-type — стандарт.
- `response_model` vs return-type annotation: FastAPI 0.99+ умеет читать return type с `-> BotRateResponse`. `response_model` — explicit override.

## 3.8 Streaming, WebSockets

(На случай follow-up)
- `StreamingResponse(generator)` — chunk-by-chunk, для больших payloads.
- `WebSocket` — `@app.websocket("/ws")`, full-duplex. ASGI-native.
- Server-Sent Events — через `StreamingResponse` с `media_type="text/event-stream"`.

## 3.9 Why FastAPI подходит для MCP-сервера

- ASGI = native async, well suited для I/O-heavy integration layer.
- Pydantic = native schema generation (MCP needs JSON Schema для tool args).
- DI = clean injection of upstream clients/credentials.
- OpenAPI autogen — близко по духу к tool-schema list/call.
- Минус: MCP transport нативно — stdio + Streamable HTTP; FastAPI сам по себе — только HTTP. Для stdio transport нужен separate adapter (e.g., `FastMCP` обрабатывает). См. Блок 4.

---

# Блок 4. System design — под роль MCP Integration Layer

## 4.1 API Design-принципы (как ты проектировал и как должен)

### REST-принципы
- **Resource-oriented**: существительные в URL (`/tasks/{id}/comments`), не глаголы (`/getTaskComments`).
- **Stateless** на серверной стороне (между запросами — но auth-токеном сохраняется сессия).
- **HTTP methods** semantically: GET — safe + idempotent, PUT — idempotent, POST — non-idempotent (по умолч.), DELETE — idempotent.
- **Status codes**: 2xx success, 4xx client error, 5xx server error. Не 200-with-error-in-body (моя `BotRateResponse` 200 с `status=ERROR` — это **антипаттерн по REST**; честно: для agentic systems структурированный error envelope релевантнее, чем HTTP-семантика, но это trade-off).

### Idempotency keys (the key pattern для tool-API)
```
POST /tools/{tool}/call
Headers: Idempotency-Key: <uuid>
```
- Сервер хранит `(idempotency_key, request_hash, response, status)` в Redis/Postgres с TTL (24h–7d).
- Повторный запрос с тем же key: если в обработке — верни 409 или 202; если задание завершено — верни сохранённый response (тот же статус и тело).
- Если requestId другой с тем же контентом — обрабатывай как fresh.

**У меня примитивно:** `tasks_queue` (in-process list) дедупит по `task_id` (`app.py:595`). Не персистентный, не cross-process. **Улучшение:** Redis `SETNX` на `botrate:{request_id}` с TTL для persistent idempotency.

### Versioning
- URL versioning: `/v1/`, `/v2/` — STILL популярно (HTTP API). AWS этим пользуется.
- Header-based: `Accept: application/vnd.acme.v2+json`.
- Для tool-API: схема tool'а version'd (e.g., `tool_name@v1`), и `result.schema_version`. Когда логика агента и интеграция эволюционируют независимо — version-lock критичен.

### Error envelope
```
{ "error": { "code": "LIMIT_EXCEEDED", "message": "...", "details": {...}, "retryable": true, "retry_after_ms": 1000 } }
```
- `retryable` — **ключевое** для агентов: LLM должна знать, можно ли retry'нуть.
- `code` — машиночитаем; `message` — для человека/LLM-рассуждения.
- У меня: `UserError(...)` propagated from `wrapper()` (`utils/wrapper.py`), в `/botrate` оборачивается в `BotRateResponse(message=text)` — полуstructured. Improvement: unified error envelope.

### Content filtering / access control for retrieval-augmented agents
- У меня: `filter_khub_docs_by_access(...)` (`single_prompt.py:433-453`, `prisma_agent.py:622-632`) — фильтрует retrieved KHub-документы по AD-группам автора задачи. Это **access-controlled RAG** — pattern, ключевой для enterprise AI.
- Принцип: retrieval → filter by principal → return. Это **post-filter**; минус — отдаёт меньше чем top-k после фильтрации (BIAS в результатах поиска). Лучше: **pre-filter** (RLS — Row Level Security на стороне поиска). На интервью: «post-filter — pragmatic; pre-filter — production; я выбрал post-filter из-за отсутствия hooks в KHub API».

## 4.2 Reliability patterns

### Retry + Exponential backoff + Jitter
- Linear: `sleep(N)` — bad. **Exponential**: `base * 2^attempt`, capped.
- **Jitter** (prevent thundering herd): `sleep = min(cap, base*2^attempt) + random(0, jitter)`. AWS-style «decorrelated jitter» — `sleep = min(cap, rand(prev_sleep/3, prev_sleep*3))`.
- Cap: total retry budget timeout. Don't retry forever.

**У меня (`httpx_async.py:205-209`):** `await asyncio.sleep(attempts_timesleep)` — FIXED 7s sleep. **Без exponential, без jitter.** Честная самооценка: «7s fixed подбирался эмпирически под LLM-Integration, exponential + jitter был бы правильнее — это улучшение, которое я запланировал».

### Retry policy: when to retry vs fail
- Retry: 5xx, connection errors, timeouts (transient).
- Don't retry: 4xx (except 429, 408, 425), parser errors.
- 429: respect `Retry-After`, если есть; иначе exponential.

**У меня**: 429 — escalate priority low→normal→high (`httpx_async.py:85-93`), не retry на той же модели — правильно. 4xx кроме 429 — немедленный return (`httpx_async.py:159`). 5xx — retry. Это **correct retry policy** — упомяни как успех.

### Circuit breaker
3 состояния: **closed** (passes), **open** (fast-fail) после N failures в окне, **half-open** (probe request). Library: `pybreaker`, `aiobreaker`. Без CB — каскадные отказы.

**У меня нет явного circuit breaker** — упомяни как future improvement, особенно для LLM-Integration: если LLMIS упал на 5+ минут, должен fast-fail agent calls, а не retry и timeout на каждый запрос.

### Bulkhead
Изолируй ресурсы: один leaky upstream не съедает пул коннектов остальных.
- Separate connection pools per upstream.
- `httpx.AsyncClient` с собственным пулом на каждого клиента — у меня так и есть (отдельный `AsyncClient` в каждом `__init__`; для тонкого контроля — `httpx.Limits(max_connections=...)`).

### Rate limiting
- **Token bucket**: capacity `b`, refill rate `r` tokens/s; consume 1 per request; if bucket empty — 429.
- **Fixed window**: count per second/minute. Edge: burst на границе окна.
- **Sliding window**: weighted avg of current and prev window — smooth.
- **Leaky bucket**: smooths output rate (queues).
- Для **outbound** rate limit (когда мы вызываем LLM-Integration) — Token bucket.
- Для **inbound** (защита /botrate) — sliding window через Redis.

**У меня outbound rate control — partial**: 429 escalation + retry — reactive, не proactive. Proactive: token bucket — просим лимиты у `/api/v1/systems/limits` (`llm_integration.py:212`), предсчитываем. Improvement.

### Timeout budget
- Общий deadline запроса = сумма всех retry timeouts downstream.
- У меня: `AsyncClient(timeout=60.0)` для upstream; `LLMIntegration` отдельно 180s. **Per-request timeout × retries = max 5×180s = 15 min на запрос**. Это trade-off; для агентов это много; лучше — `connect=5, read=60` per attempt, и overall request timeout на agent-orchestrator'е.

## 4.3 Observability

### Three pillars
1. **Logs** — structured JSON (у меня через `LogFormatter` `utils/logger.py:14`, в stdout + Graylog GELF UDP). **Уровни: DEBUG → file (only if fs writable), INFO+ → stdout.** В K8s `readOnlyRootFilesystem` → file-логирование off (`logger.py:61`).
2. **Metrics** — quantitative time-series. RED (Rate, Errors, Duration) for services; USE (Utilization, Saturation, Errors) for resources.
3. **Traces** — distributed request flow across services. OpenTelemetry — стандарт.

### У меня observability
- Logs: structured JSON, `ContextVar` `logging_context` (`logger.py:10`) — correlation (task_id, source, prompt_id) propagируется в каждый log line. **Это правильно — correlation-ID pattern.**
- Metrics: Kafka stream (`KafkaClient.send_botrate_metric`, `botrate_agent.py:704`), downstream aggregation. RAGAS online eval (faithfulness, groundedness) — **production LLM-as-a-judge**: 2 extra LLM calls per request (`AGENTS.md:166`).
- Traces: **отсутствуют**, минус. Improvement: OpenTelemetry instrumentation (`@tracer.start_as_current_span()`) per tool-call — особенно для MCP, где trace = цепочка вызовов tools.

### Что инструментировать на каждый tool-call (релевантно роли)
- tool_name, version, caller_id (agent)
- request_count, error_count (RED)
- latency histogram: per-read / per-write
- upstream response codes (per status class)
- timeout occurrences, retry counts, fallback-events
- business outcome (наш `BotrateMetric.action` / `is_final`)
- token usage, если LLM

### SLI/SLO
- SLI (Service Level Indicator): "fraction of requests succeeded in <500ms" = good/total.
- SLO: target = 99% requests succeed in <500ms. Error budget = 1%.
- SLA: contractual, subset of SLO.
- Для integration layer — SLO на латентность: p95 per-tool, p99 overall.

## 4.4 Contract testing

### Pact (consumer-driven)
- Consumer пишет «expectations» (request → expected response) → test contract.
- Provider запускает этот contract — подтверждает, что его API удовлетворяет.
- Catch breaking changes **before deploy**.

### У меня подход
- Pydantic-модели как runtime-контракт (request body validated automatically).
- OpenAPI auto-gen — «тестирование spec против ответов».
- **No formal Pact** — улучшение. «Я понимаю ценность consumer-driven contracts для platform layer: агенты договорились, что `tool_x` возвращает `KHubResult`-shape; формальный Pact провалил бы релиз, если бы я изменил schema».

### SDK ergonomics / schema evolution
- Additive changes (new optional fields) — forward-compatible.
- Removing/renaming fields, changing types — breaking.
- **Versioning strategies**: backward (new optional field, old clients still work), forward (new optional field, new clients accept old responses).
- **The "expand, don't break" principle**: rename → add new → dual-write → deprecate → remove.

## 4.5 MCP — Model Context Protocol (глубоко)

### Что это
- Anthropic-зарождения, **open protocol** для связи LLM-applications ↔ external tools/resources.
- Спецификация: https://modelcontextprotocol.io (версия 2025-06-18 — текущая на момент интервью).
- Аналог: LSP (Language Server Protocol) адаптирован для DevTools. MCP — для AI agents.
- Решает: каждый LLM-vendor имел свой tool-calling API; MCP унифицирует «как агент обнаруживает инструменты, какие у них schemas, как их вызывать».

### Архитектура MCP
- **MCP Host** — приложение, в котором работает LLM (Claude Desktop, IDE, votre custom agent).
- **MCP Client** — встроен в host, один клиент на один MCP server.
- **MCP Server** — standalone-процесс, выставляет capabilities (tools/resources/prompts).
- **Transport** — способ доставки JSON-RPC 2.0 сообщений:
  - **stdio** — subprocess + stdin/stdout. Local usage (IDE-plugins).
  - **Streamable HTTP** (пришёл на смену SSE в 2025-06-18) — single `/mcp` endpoint; POST для client→server requests, GET/POST для server→client (SSE-based subscriptions). **HTTP = remote-hosted**.
  - **WebSocket** — historical, deprecated.

### MCP lifecycle (обязательно знать)
1. **Initialize**: client → server, `initialize` JSON-RPC с `protocolVersion`, client capabilities, client info. Server ответит своим `capabilities` + `serverInfo`. **Capabilities** = какие features server поддерживает (tools/resources/prompts/logging/sampling/roots).
2. **Initialized notification**: client → server, `initialized` — фаза завершена.
3. **Discovery**:
   - `tools/list` → server возвращает массив `[{name, description, inputSchema}]`. **inputSchema = JSON Schema** (draft 7) — то же, что FastAPI/Pydantic генерирует.
   - `resources/list` → static-ish files (`{uri, name, description, mimeType}`).
   - `prompts/list` → пользовательские prompt-templates.
4. **Invocation**:
   - `tools/call` с `{name, arguments}`. Server ответит `{content: [...], isError: bool}`. Content-typed: text, image, resource-link.
   - `resources/read` по `uri`.
   - `prompts/get` по name, возвращает ready messages.
5. **Server→client requests** (опционально):
   - **Sampling** (`sampling/createMessage`) — server просит client'а создать LLM-ответ (e.g., tool просит LLM для summarization). Это **agentic**: tool сам может вызывать LLM через host'а.
   - **Roots** (`roots/list`) — client даёт server доступ к файловым/ресурсным «корням» (workspace boundaries).
6. **Shutdown**: для HTTP — просто закрыть соединение; для stdio — process exit.

### Полный JSON-RPC пример `tools/list` response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_pyrus_task",
        "description": "Fetch a Pyrus task by its numeric ID",
        "inputSchema": {
          "type": "object",
          "properties": { "task_id": { "type": "integer", "description": "Pyrus task id" } },
          "required": ["task_id"]
        },
        "annotations": {
          "readOnlyHint": true,
          "idempotentHint": true
        }
      }
    ],
    "nextCursor": null
  }
}
```
- **`annotations`** (новое в 2025-06-18) — hints для LLM о свойствах tool: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. **Именно это явное перечисление idempotency для агентов — релевантно вакансии.**

### Tool-результат
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [ { "type": "text", "text": "..." } ],
    "isError": false
  }
}
```
- Error **НЕ JSON-RPC error-level** — это `isError: true` с content, описывающим ошибку. **JSON-RPC-level error** только для protocol-level mistakes (unknown method, bad params). Это важно: agent видит `isError` и **reasons** (не просто retry) — ergonomics.
- Structured output (optional `structuredContent`) — typed result schema для программы.

### Security
- Authentication: **Streamable HTTP** supports OAuth 2.1 (новое в 2025-06-18) — Authorization header `Bearer`, возможна dynamic client registration. У MCP stdio — implicit trust (local process).
- **Resource isolation**: roots ограничивают доступ server'а к данным клиента.
- **User consent** для sampling: `sampling/createMessage` требует user prompt confirmation в UI.
- **No implicit tool execution**: agent всегда может спросить user'a → HITL pattern.

### FastAPI как MCP-сервер

**Два способа:**

**Option A: Использовать `FastMCP` (Python SDK)**
```python
from fastmcp import FastMCP
mcp = FastMCP("salmon-integrations")

@mcp.tool
async def get_pyrus_task(task_id: int) -> str:
    """Fetch a Pyrus task by id."""
    client = PyrusClient(...)
    return await client.get_task_info(task_id)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```
- `inputSchema` автоматически из signature + docstring.
- underlying — Starlette ASGI, т.е. **FastMCP уже FastAPI/Starlette-based**.
- Transports: `stdio`, `http` (Streamable HTTP), `sse` (legacy).

**Option B: Обернуть существующий FastAPI-сервис**
Если как у меня — уже есть FastAPI-приложение с логикой, то:
1. Выдели интеграционные операции в `@tool`-функции (см. выше).
2. Поднимай `FastMCP` рядом (или import твоих клиентов) — expose как MCP tools.
3. **Возможна co-location**: FastMCP-server в одном process с FastAPI, разные ports/paths — они шарят модули `clients/`, `functions/`.

### Маппинг `summarizer-it` → MCP tools (твой killer answer)

| Текущий URL/Path | MCP tool name | MCP capability |
|---|---|---|
| `POST /webhook_handler` | `pyrus_process_task` | tool с `task_id` input, async; **не readOnly** (пишет комментарии в Pyrus); annotations: `idempotentHint: true` (по `task_id` + dedup), `destructiveHint: false`. |
| `PyrusClient.get_task_info` | `pyrus_get_task` | `readOnlyHint: true`, `idempotentHint: true` |
| `AsyncConfluenceClient.search` | `confluence_search` | `readOnlyHint: true` |
| `JayKHubClient.send_message_async` | `khub_query` | `readOnlyHint: true` |
| `KeycloakClient.verify_token` | — внутренний (не для LLM, auth) |
| `process_selected_prompt` с `order`-прогрессией | multiple tools, либо **state machine tool** (high-level agent primitive) |
| `LLMIntegration.get_completions` | **`sampling/createMessage`** — server просит host's LLM, **agentic** pattern, экспериментальный |

Это **прямое применение твоего кода**. На интервью сообщи: «вот, я бы взял мой `summarizer-it`, добавил `FastMCP`-обёртку над существующими клиентами и получил бы готовый MCP-сервер для агентов».

### Минимальный код-скелет (важно — для follow-up «напиши как»)
```python
from fastmcp import FastMCP
from clients.pyrus import PyrusClient
from clients.confluence import AsyncConfluenceClient

mcp = FastMCP("salmon-integrations")

@mcp.tool(annotations={"readOnlyHint": False, "idempotentHint": True})
async def pyrus_post_comment(task_id: int, text: str) -> str:
    """Post a comment to a Pyrus task. Idempotent by task_id+text hash."""
    async with PyrusClient(config) as pc:
        resp = await pc.update_task(task_id=task_id, req_body={"formatted_text": text})
    return resp or {"status": "failed"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

### Что нового в spec 2025-06-18 (для «are you following it?»)
- **Streamable HTTP** заменил SSE-single transport (single endpoint `/mcp`, POST для client→server, GET/SSE для notifications).
- **OAuth 2.1** authentication для remote MCP (auth flow с dynamic client registration).
- **Tool annotations** (`readOnlyHint` и др.) — make properties visible to LLMs.
- **`structuredContent`** — typed structured output (vs only text).
- **Resource templates** — URI templates parametrized (`pyrus://tasks/{task_id}`).
- **Elicitation** — server может ask user'a уточняющий вопрос (callback из tool invocation).

## 4.6 AWS / EKS / Terraform (концептуально, для пробела)

### EKS-specific
- EKS = managed control plane (API server, etcd) by AWS; worker nodes = EC2 (managed node groups) или Fargate (serverless pods).
- IAM-roles-for-service-accounts (IRSA) — pods используют IAM role через OIDC federation (vs static creds). Это эквивалент Vault-AppRole у меня, только native AWS.
- ALB Ingress Controller; Network policies via Calico/Cilium.
- VPC CNI — каждый pod получает VPC-routable IP; subnet sizing matters.
- CloudWatch logs, X-Ray traces (OpenTelemetry-compatible).

- **Мой K8s-опыт переносится**: Helm charts (`helm/values-prod.yaml`), `readOnlyRootFilesystem: true`, Vault-secrets — концептуально те же. Только Helm → Helm on EKS via `helm install` to cluster с IRSA; secret store через External Secrets Operator + AWS Secrets Manager (альтернатива Vault).

### Terraform
- IaC: declarative `resource "aws_eks_cluster" {...}`, plan → apply.
- `terraform state` persisted в S3 (+ DynamoDB lock).
- Modules — reused. `eks` module canonical.
- Concepts: providers, resources, data sources, variables, outputs, state, plan/apply/destroy.
- Drift detection: `terraform plan` показывает diff.
- Альтернативы: Pulumi (Python), CDK (AWS-only), Crossplane (Kubernetes-native).

**Позиционирование:** «Я знаю концепции IaC через Helm и GitLab CI variables; Terraform я понимаю на уровне diagram, но не использовал в проде. Прямо сейчас fast-track изучаю AWS foundational services и Terraform basics за неделю. Мне хотелось бы, чтобы infra-as-code была частью практики команды.»

## 4.7 Пример system design question (для репетиции перед интервью)

> "Спроектируй MCP-server, который выставляет 20+ инструментов поверх internal API, на 1000 RPS agent calls."

**Walkthrough:**
1. **Transport**: Streamable HTTP (remote), one `/mcp` endpoint.
2. **Process model**: stateless HTTP servers; horizontal scaling behind ALB. **Sticky session no** — except sampling (long-lived). For sampling — WebSocket upgrade.
3. **Tool registry**: in-code (if stable) или in DB `tools`-table (if dynamic — adds/removes без redeploy). Per-tool config: auth scope, rate limit, timeout budget, annotations.
4. **Auth**: OAuth 2.1 Bearer; per-tool scope в token; map token→principal; row-level filtering на tool level (мой `filter_khub_docs_by_access`).
5. **Rate limiting**: per (principal, tool) Token Bucket в Redis (sliding window в продакшн).
6. **Circuit breaker** per upstream tool (`pybreaker`).
7. **Idempotency**: idempotency-key header, storage в Redis 24h.
8. **Backpressure**: bounded `asyncio.Queue` + Semaphore per upstream; reject 429 с `Retry-After` на лимит.
9. **Observability**: OpenTelemetry — trace span на tool call (tool name, version, principal, duration, error); RED metrics; structured logs with correlation.
10. **Schema evolution**: per-tool version в name (`get_task@v1`); deprecated tools removed per policy; additive changes only.
11. **Contract testing**: Pact per tool — consumer (agent) expectations; provider (ваш server) replayed в CI.
12. **HITL**: для destructive tools — MCP elicitation или sampling consent.
13. **Resilience**: deploy blue-green; k8s readiness probe; retriable 5xx идёт на другой pod через LB.

---

# Блок 5. Пробелы — заготовки (без вранья)

### Q: «У вас 5+ лет Python?»
> «Честно: формально на Python как основном языке я работаю последние 3 года. До того 4+ года SRE — писал скрипты автоматизации, участвовал в incident response на платформе с 40+ микросервисами, где Python присутствовал, но мой фокус был эксплуатация. Это научило меня production-мышлению — что код должен дежуриться, что failures — норма, что observability важна. Поэтому, когда я перешёл в разработку, я сразу писал код с retry, structured logging, idempotency. По совокупности практического опыта я соответствую senior expectations, но честно говорю, что классический «академический» стаж 5+ лет Python у меня — 3 года.»

### Q: «У вас есть опыт с MCP?»
> «Прямо — нет. Но я построил эквивалентный integration layer в `summarizer-it`: FastAPI-сервис, через который LLM-агенты (`LangGraph` agents, chatbot widget /botrate) вызывают 11+ internal API (Pyrus, Confluence, KHub, Minerva, Graylog, etc.) с retry, priority escalation, fallback, structured error-envelope, access-controlled retrieval. Принципы проектирования идентичны MCP: schema clarity для LLM, idempotency для safe retries, error identification. Я прочитал спецификацию MCP 2025-06-18: lifecycle initialize/initialized → tools/list → tools/call, JSON-RPC 2.0 over Streamable HTTP, tool annotations (`readOnlyHint`, `idempotentHint`), OAuth 2.1 auth. Я знаю, как FastAPI ложится на MCP через `FastMCP` — обернуть существующие клиенты в `@mcp.tool`-декораторы, не переписывая интеграционный слой. Могу первую же неделю поэкспериментировать с этим широко.»

### Q: «AWS опыт?»
> «К сожалению, прямого AWS-опыта в production у меня нет. Мой K8s-опыт — на собственных/vm-инфраструктурах. Однако концепции, которые я использую ежедневно — Helm, Vault AppRole secrets, GitLab CI, readOnlyRootFilesystem, IRSA-эквиваленты, observability через Grafana/Graylog — маппируются directly на EKS. Прямо сейчас изучаю AWS foundational services (VPC, EKS, IAM, Secrets Manager, CloudWatch) и могу запустить demo на EKS в течение ~1–2 недель. Самая сложная часть — K8s operations, что я уже хорошо знаю. Операции на EKS — это правильно сконфигурированный Terraform + Helm, мне хорошо знакомый.»

### Q: «Terraform?»
> «Не писал на Terraform в production, но понимаю IaC declarative paradigm, потому что Helm charts — это, по сути, IaC для K8s. Я видел Terraform modules, понимаю state-file, providers (aws/kubernetes). У меня от SRE-роли есть сильная база для декларативного config-management. Я могу начать продуктивно использовать Terraform в short timeframe — неделями, не месяцами.»

### Q: «Contract testing?»
> «Я не использовал формальный Pact-style-фреймворк. Эквивалентно я построил: Pydantic-модели на каждой API-границе как runtime-контракт; FastAPI auto-gen OpenAPI; для каждого external service пишу integration tests, которые проверяют request/response shape versus реальный upstream. Я понимаю ценность consumer-driven contract testing для platform-layer, особенно когда агенты develop independently от tool implementation. Pact был бы правильным addition.»

### Q: «Вы были on-call?»
> «4+ года SRE на banking platform (40+ микросервисов, 99.9% SLA). Был part of incident response, root cause analysis, использовал active dashboards и proactive alerting. Не "on-call rotation" в западном смысле, но схожие expectations по reaction. В `summarizer-it` я owner end-to-end — от сбора бизнес-требований до investigate production issues (LLM-fallback при rate-limit, traceback errors через Graylog).»

### Q: «У вас нет CS-образования. Что это значит?»
> «Я самоучка — диплом маркетинг, перешёл в IT через сертификаты и hands-on. Я честно признаю пробелы в formal CS — algorithmic theory, complexity analysis на формальном уровне. Я закрываю их target-by-target: когда нужно отлаживать concurrency-проблему — учусь details event loop; когда оптимизировать GC — учусь gc internals; когда schema evolution — API versioning standards. My advantage — продуктовое мышление (из маркетинга): я собираю requirements, измеряю impact в бизнес-терминах (сэкономленные часы, авто-разрешённые тикеты), и это хорошо для platform mindset, где users — другие инженеры.»

### Q: «Как вы используете AI в работе?»
> «Я использую AI как brainstorm-партнёра и ревьюера: когда faced с non-trivial design decision, я прошу у AI pros/cons; для research инструментария; для code-review sanity. Все финальные решения и ответственность — мои. Я знаю, что для platform-интеграций, где нужна точность и deep domain understanding, AI ускоряет, но не заменяет — особенно edge cases, auth flows, concurrency.»

---

# Блок 6. Банк вопросов (репетируй вслух)

> Подсказка: каждый ответ — 30–90 секунд. Прежде чем отвечать — пауза 1–2 секунды. Если не знаешь — говоришь: «Честно: глубоко это не знаю, но моя интуиция подсказывает...» затем best-effort.

### Q1. «Расскажите про архитектуру вашего основного проекта»
> summarizer-it — FastAPI-сервис с 3 эндпоинтами: POST /webhook_handler (Pyrus events), POST /botrate (BotRate widget), GET /health. Main flow: Pyrus посылает webhook → я добавляю его в BackgroundTasks (`background_tasks.add_task(handle_webhook, pyrus_event)`), немедленно отвечаю `{"data_received":"ok"}` → в фоне `handle_webhook` lookup промпта в реестре (`find_multiprompts`) → если несколько промптов с `order` — вход в `prompts_loop` (`while True`, обновляю состояние задачи после каждого промпта с fallback на `get_task_info`) → каждый промпт = `process_selected_prompt` (сбор контекста: task fields, Confluence, KHub, Minerva, Graylog, параллельно через Prisma agent на LangGraph StateGraph + Send API → LLM → post результата обратно в Pyrus/email/VK Teams). Observability: structured JSON logging с correlation через ContextVar, Kafka stream для бизнес-метрик, RAGAS online eval. Auth: Keycloak OAuth на /botrate с JWKS/RS256 + AD-group filtering на retrieved docs. Deploy: Docker, GitLab CI, K8s (Helm) или VM.

### Q2. «Почему вы выбрали FastAPI?»
> ASGI + native async под I/O-heavy нагрузку (моё приложение 80% времени ждёт LLM/HTTP upstream). Pydantic даёт мне strict-typed boundary и auto-gen OpenAPI/Swagger. DI через `Depends` (частично использую, частично globals — improvement-зона). Starlette's middleware/handlers принимают custom exception handler на `RequestValidationError` (для моего `/botrate`). Альтернативу я рассматривал aiohttp, но у Pydantic v2 + типы = короче код, и auto-docs/Swagger для platform users (инженеров) ценно.

### Q3. «Что делает `wrapper()`?»
> Это централизованный async error-handler (`utils/wrapper.py`). Принимает coroutine function + kwargs, await'ит, ловит `HTTPError`, `JSONDecodeError`, `UserError` (custom), `CheckPromptResult` (control-flow exception), `AttributeError`, `ValidationError`, generic `Exception`, bare `except`. Решает per-типу: логировать + вернуть `None` (HTTP, JSON, validation), пробросить с логированием (`UserError` из non-app.py files), обернуть в generic `UserError` (из app.py с non-UserError context). Проблема, которую я знаю: bare `except` проглатывает всё — это code smell, в refactor я бы ловил конкретные типы. В реальном проекте это дало централизацию для 11+ клиентов без дублирования.

### Q4. «Как у вас устроен retry?»
> Base class `AsyncHTTPClient.request()` (`utils/httpx_async.py:32`): 5 attempts, fixed 7s sleep между ними, выбран эмпирически. Retry policy: 5xx → retry; 4xx (except 429) → no retry, immediate return. **429 от LLM-Integration** — особый кейс: escalate priority `low → normal → high`, на exhaustion — fallback от `qwen3-30B` к `expert` (`httpx_async.py:215-219`). ReadTimeout на LLMIS → raise `UserError`. Я знаю, что proper exponential backoff with jitter был бы правильнее — improvement. Также я бы ввёл per-upstream circuit breaker (`pybreaker`) для случая, когда upstream совсем down → fast-fail вместо 5 retries × 180s timeout.

### Q5. «`await asyncio.gather(*coros)` что вернёт, если одна задача упадёт?»
> По умолчанию — fail-fast: первая exception пробросится из gather. **Другие Tasks остаются живы** (не отменяются) — common gotcha. Решение: `gather(*coros, return_exceptions=True)` — все exceptions возвращаются как значения в result-list. Альтернатива: `asyncio.wait` — возвращает `(done, pending)` и можно явно решать, что делать с pending. У меня gather явного нет, но LangGraph's Send API под капотом concurrent-style — он аккумулирует через reducer `Annotated[list, operator.add]` (`botrate_agent.py:241`), успешно completed и failed-результаты смешаны в `khub_results`.

### Q6. «Когда вы бы использовали threading vs asyncio?»
> asyncio — для I/O-bound с большим concurrent-ом (моё приложение). threading — когда есть блокирующие sync-библиотеки, у которых нет async API (python-ldap, hvac по местам); в этом случае `asyncio.to_thread` учитывает, что тред блокируется на I/O — GIL не мешает (тред спит на socket), loop крутится параллельно. multiprocessing — только для CPU-bound (парсинг больших docs, embeddings на CPU); у меня CPU-bound нет — всё тяжёлое на LLM-Integration. Важно: asyncio — concurrency, не parallelism — внутри одного треда никогда не исполнит две инструкции одновременно.

### Q7. «Что такое GIL?»
> CPython — single mutex на интерпретатор: в любой момент ровно один thread исполняет Python bytecode. Switch — каждые 5ms и при I/O. Следствие: threading не ускоряет CPU-bound Python — для этого multiprocessing (отдельные интерпретаторы — отдельные GIL). Для I/O-bound GIL не мешает — треды спят на syscalls. PEP 703 — experimental no-GIL в 3.13. У меня весь проект asyncio — GIL не bottleneck, т.к. всё I/O-bound.

### Q8. «Как работает Garbage Collection Python?»
> 1) Reference counting — primarily, every PyObject has `ob_refcnt`, при достижении 0 — немедленный collect (детерминированно, в отличие от Java). 2) Generational cyclic GC для разрыва ссылочных циклов (A→B→A), 3 generations, младшая сканируется чаще. 3) `__del__` finalizer — проблематичен, может блокировать cyclic GC (PEP 442 в 3.4 починил — теперь cycles с `__del__` собираются). У меня есть `__del__` в `AsyncHTTPClient` (`httpx_async.py`) для логирования — это code smell; в продакшн лучше явный `async with` через context manager, что я и делаю для `JayKHubClient` (`botrate_agent.py:371`).

### Q9. «Pydantic v1 vs v2 — что нового?»
> v2 — Rust core (pydantic-core), в 5–50x быстрее. `.dict()` → `.model_dump()` (с `mode='json'` для JSON-native serialization, datetime → ISO). `.parse_obj()` → `.model_validate()`. `@validator` → `@field_validator`/`@model_validator`. `Config` inner class → `model_config = ConfigDict(...)`. `Annotated[int, Field(gt=0)]` — modern style. У меня `model_dump(mode='json')` для `BotRateResponse` (`app.py:1098`), Enum через `str, Enum` для JSON-serializable обязательно.

### Q10. «Что Pydantic-модель реально делает в FastAPI?»
> Когда FastAPI видит типизированную param как `request: BotRateRequest` в endpoint-е, он: (1) читает request body, (2) запускает Pydantic validation, (3) при ошибке поднимает `RequestValidationError` (по умолчанию → 422), (4) если ОК — передаёт мне валидный объект. И outbound — через `response_model` проходит через Pydantic для schema-filtering и serialization. У меня custom exception handler `botrate_validation_exception_handler` (`app.py:80`) для `/botrate` разворачивает 422 → 400 + `BotRateResponse` со `status=VALIDATION_ERROR` — эргономично для вызывающего-агента.

### Q11. «`BackgroundTasks` vs `asyncio.create_task` — что выбирать?»
> `BackgroundTasks` — Starlette-фича: запускается после response в том же event loop, гарантирует, что ответ отошёл первым. Минус: in-memory, single-process, потеряется при рестарте/crash, не масштабируется через workers. `create_task` запускает немедленно, не связан с request-lifecycle — подходит для фоновых jobs через `lifespan` (как мой `llm_limits_monitor` `app.py:67`). Для production-critical — external queue (Celery/RQ/RabbitMQ/Kafka). У меня Pyrus re-delivery вебхуков компенсирует потерю; это известное ограничение.

### Q12. «Как вы обеспечиваете идемпотентность в tool-API для агентов?»
> 1) Idempotency-Key header (`Idempotency-Key: <uuid>` — стандартный pattern, как Stripe API). Сервер хранит `(key, request_hash, response, status)` в Redis с TTL 24h. 2) Повторный запрос с тем же key → тот же response или 409, если in-flight. 3) Tool annotations в MCP — `idempotentHint: true` — LLM знает, что retry безопасен. 4) Server-side natural idempotency where possible — `update_task` (set field) идемпотентен; `create_task` — нет, требует key. У меня примитивно: in-process `tasks_queue`-дедуп по `task_id` — но не cross-process, не persistent. Improvement: Redis `SETNX idempotency:{tool}:{key}` с TTL.

### Q13. «Что такое MCP и как он работает?»
> Model Context Protocol — open-спецификация от Anthropic, унифицирующая, как LLM-агенты обнаруживают и вызывают tools/resources/prompts. JSON-RPC 2.0 поверх stdio или Streamable HTTP. Lifecycle: client → server `initialize` (protocolVersion + capabilities) → `initialized` notification → `tools/list` (response: array of tools с JSONSchema input) → `tools/call` (`{name, arguments}` → `{content, isError}`). Server может request sampling (`sampling/createMessage`) от host's LLM — это agentic pattern. Auth для remote: OAuth 2.1 (novое в 2025-06-18). Tool annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` — помогают LLM в рассуждениях.

### Q14. «Как бы вы обернули `summarizer-it` в MCP server?»
> Использовать **FastMCP** — Python SDK поверх Starlette/ASGI. Каждый мой существующий клиент (`PyrusClient`, `AsyncConfluenceClient`, `LLMIntegration`) — обернуть его methods через `@mcp.tool`-декоратор. `inputSchema` автоматически из сигнатуры + docstring. Annotations: `pyrus_get_task` — `readOnlyHint=True, idempotentHint=True`; `pyrus_post_comment` — `idempotentHint=True` по hash content; `pyrus_create_task` — `destructiveHint=True`. Transport: streamable-http, port 8000 parallel с existing FastAPI. Аутентификация через OAuth 2.1 + мой existing Keycloak verifyer. **Никакого переписывания integration-логики** — сам service-layer остаётся.

### Q15. «Как бы вы спроектировали новый tool в этом integration layer?»
> 1) Define schema (Pydantic v2) — input args + output shape. 2) Annotate with hints (readOnly/idempotent/destructive). 3) Use `AsyncHTTPClient`-subclass с retry (exponential + jitter + circuit breaker), custom auth, rate limit via token bucket на клиент-стороне. 4) Document tool description для LLM (чёткое, без двусмысленностей). 5) Pytest tests including contract tests vs upstream API. 6) Structured logging with correlation. 7) RED-metrics (rate/errors/duration per tool). 8) Idempotency-key handling. 9) Schema versioning (`tool_name@v1`). 10) Deploy — K8s/Helm, rollout blue-green, readiness probe. Это как раз то, что я раньше уже делал добавлением нового Pydantic-модели + клиента в `clients/`, просто с MCP-обёрткой как discovery/call surface.

### Q16. «Как вы справляетесь с идемпотентностью при параллельных вебхуках на одну задачу?»
> Сейчас — in-process `tasks_queue` list (`app.py:139`) + `await asyncio.sleep(2.5)` перед `if task_id in tasks_queue` (`app.py:595`). Это poor-man's lock, полагающийся на single-threaded event loop. Limits: 1) Не cross-process (при uvicorn --workers 2 — гонка между workers); 2) Не persisted (рестарт теряет состояние очереди); 3) не real lock — read-check-append не атомарно даже в asyncio без `Lock`. Production solution: Redis `SETNX lock:pyrus:{task_id}` с TTL; idempotency-key на операцию; per-task version/ETag для optimistic concurrency. Я понимаю проблему и решаю при необходимости.

### Q17. «Как вы управляете Keycloak токеном — refresh logic?»
> `KeycloakClient.upgrade_client(client_to_upgrade)` (`keycloak_client.py:77`): запрос токена client_credentials, установка `kc_token_exp_dt = now + expires_in - 900s` (15 мин запас). Перед каждым вызовом LLM/N8N — `await wrapper(keycloak_client.upgrade_client, client_to_upgrade=llm_integration)` — проверяет expired ли, refresh'ит, обновляет Authorization header на целевом клиенте. Глобальные `llm_integration`, `keycloak_client`, `n8n_client` обновляются с возвращёнными значениями (`prompts_loop.py:246-248`). JWKS — `PyJWKClient` с `cache_keys=True, lifespan=3600, max_cached_keys=16` — cached, не рефетчит каждый раз. Параллельно детектится ротация ключа: сравнивается `kid` с `_last_known_kid` (`keycloak_client.py:125`).

### Q18. «Как у вас observability устроена?»
> 1) Structured JSON logging (`utils/logger.py:14`, `LogFormatter`) — в stdout и optional в `./data/logfile.json` (DEBUG only, disabled на K8s `readOnlyRootFilesystem`). Plus Graylog GELF UDP (`logger.py:71`). 2) **Correlation через ContextVar** `logging_context` (`logger.py:10`) — task_id, source, prompt_id propagируется в каждый `logger.info()` через `extra={}`. `LogFormatter` reads from contextvar. 3) Kafka stream для бизнес-метрик (`KafkaClient`, `botrate_agent.py:692`), downstream aggregation. 4) RAGAS online eval (`faithfulness`, `groundedness`, `instruction_adherence`) — 2 extra LLM calls per request when enabled. **Чего не хватает — distributed tracing**; я бы добавил OpenTelemetry через `@tracer.start_as_current_span()`, особенно per-tool-call span. Латентность per-tool критична для agentic observability.

### Q19. «Что такое event loop в Python простыми словами?»
> Это single-threaded цикл, который исполняет корутины, переключаясь между ними, когда они `await` — отдают управление. В любой момент ровно одна корутина активна, остальные «приостановлены» в ожидании I/O/Future. Преимущество: тысячи конкурентных I/O-операций в одном OS-треде, без оверхеда thread-per-connection. Недостаток: один блокирующий sync-call заморозит весь loop (поэтому блокирующие либы — через `asyncio.to_thread`). Один event loop = один OS thread by default; multiple loops — per thread.

### Q20. «Чем coroutine отличается от Future/Task?»
> Coroutine — объект, который «знает как» исполняться, но не запущен (результат `async def`). Future — low-level promise result, может быть создан и не связан с coroutine. Task — Future + запланированный coroutine, создаётся через `create_task(coro)` и исполняется event loop'ом. `await x` работает с любым awaitable (объект с `__await__`) — coroutine, Future, Task. `asyncio.gather(*coros)` — внутри каждая корутина превращается в Task и собирает результаты. У меня — background `repeat_every_minute_job` через `asyncio.create_task` (`app.py:67`).

### Q21. «Можете рассказать про decorator и `functools.wraps`?»
> `@decorator` эквивалентно `f = decorator(f)`. Декоратор — callable: принимает функцию, возвращает (обычно) функцию. Без `functools.wraps` теряем `__name__`, `__doc__`, `__wrapped__` — ломается introspection, swagger. У меня декораторов не много — `@dataclass`, `@app.post`. На проекте я часто пользуюсь context manager (`@asynccontextmanager` для `lifespan`). Если бы писал custom декоратор — обязательно `functools.wraps(f)`.

### Q22. «`async with` — как работает?»
> Использует `__aenter__/__aexit__` dunder-protocol — async-version of `with`. На вход — async context manager. `__aenter__` — setup (open connection), `__aexit__` — cleanup (close), called guaranteed даже при exception, получает `(exc_type, exc_val, exc_tb)`. У меня `async with JayKHubClient(...)` (`botrate_agent.py:371`), и `lifespan` (`app.py:62`) — `@asynccontextmanager` для генераторного CM. `__aexit__` return True — suppress exception; False/None — re-raise.

### Q23. «Что делает `BackgroundTasks.add_task` точно?»
> Starlette feature: task ставится в очередь, ассоциированную с request. После return response → server вызовет task'и в порядке добавления, в том же event loop. Если task async — `await`, sync — runs in threadpool. **Не survives restart**, **single-process only** (different workers = independent). Use case — short-lived post-response work like notification, logging. Не use case — hours-long processing (лучше external queue).

### Q24. «Что такое `Annotated[list, operator.add]` в LangGraph?»
> LangGraph state-reducer spec. When node returns `{"khub_results": [item1]}`, а другой параллельный Send — `{"khub_results": [item2]}`, LangGraph комбинирует через вызов `operator.add(state["khub_results"], returned)` → `[item1, item2]`. Это immutable-style accumulator через редюсеры. Без reducer — overwrite. `operator.add` — для list-merge; можно свой custom reducer. Это pattern fan-in в LangGraph'е Send API (`botrate_agent.py:241`, `prisma_agent.py:66`).

### Q25. «Что такое `Send`-API в LangGraph?»
> Pattern для conditional fan-out: вместо строки-dest в `add_conditional_edges` вернуть список `Send(node_name, payload)` — по одному на parallel worker. LangGraph запускает workers concurrently (через `asyncio.gather` под капотом), каждый worker получает своё state payload, редюсеры комбинируют результаты. У меня `route_after_process` возвращает `[Send("khub_worker", payload) for space in SPACES]` (`botrate_agent.py:322`) — параллельные запросы к двум KHub spaces.

### Q26. «Как в `app.py` реализован контроль доступа к KHub-документам по AD-группам?»
> В `single_prompt.py` и `prisma_agent.py` после retrieval KHub-docs вызывается `filter_khub_docs_by_access(..., user_ad_groups=author_ad_groups, ...)` — фильтрует retrieved chunks по группам автора задачи. AD-группы берутся через `AsyncADClient` из LDAP по email пользователя. Это post-filter pattern (retrieved then filter) — pragmatic, когда KHub API не поддерживает pre-filter RLS. Минус: top-k может потерять релевантные chunks после фильтрации (bad recall). Better: pre-filter via KHub-native ACLs, или векторный индекс с metadata filter (Qdrant's payload filters, ...).
>
> На моей стороне это встречающийся паттерн «access-controlled RAG» — релевантно enterprise-агентским платформам, где agent видит только то, что principal имеет право видеть.

### Q27. «Расскажи про систему типов Python — что такое `Annotated`?»
> `Annotated[T, meta1, meta2, ...]` (PEP 593) — добавляет metadata к типу для runtime-потребителей (Pydantic `Field(...)`, `Annotated[int, Field(gt=0)]`, FastAPI `Annotated[int, Path(ge=1)]`). Сам type-checker всё ещё видит `T` — annotation не меняет type; metadata предоставляется tools, которые смотрят в `typing.get_type_hints(include_extras=True)`. LangGraph reducers: `Annotated[list, operator.add]` — second arg — reducer-функция.

### Q28. «Как вы тестируете FastAPI-приложение?»
> Честно: в моём проекте `pytest` есть (`tests/`), но test-suites ad-hoc, требуют corporate network/credentials. Production-tests в CI нет — это известный минус. Что я бы ввёл: 1) Fixture на `httpx.AsyncClient` через `ASGITransport` к app; 2) `pytest-asyncio` для async tests; 3) `respx` для mock upstream HTTP; 4) Property-based tests на `transform_fields_list` (hypothesis); 5) Contract tests через Pact. Работа с дополнительными test-mocks для Keycloak/JWKS.

### Q29. «Чем версия transport HTTP streamable от SSE?»
> SSE transport (older): server-sent events, однонаправленно client→server POST + server→client SSE-stream. Problem: long-lived connection per session = плохо для horizontal scaling. **Streamable HTTP** (2025-06-18): single endpoint `/mcp`, POST для client→server request, response может включать `Mcp-Session-Id` header; GET (optional, SSE) open stream — но server может drain/delete без persisting connection. Stateless-friendly = better scale. Большой выигрыш — load-balanceable на cluster level.

### Q30. «Если интервьюер: "напишите функцию `retry` с exponential backoff и jitter"»
```python
import asyncio, random
async def retry_async(func, *args, max_attempts=5, base=0.5, cap=30.0, **kwargs):
    last = None
    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last = e
            if attempt == max_attempts:
                raise
            sleep = min(cap, base * (2 ** (attempt - 1)))
            sleep += random.uniform(0, sleep * 0.1)   # jitter, AWS "full jitter"
            await asyncio.sleep(sleep)
    raise last
```
> Ключевые: **exponential** (`base * 2^(n-1)`), **cap** (avoid 1000s sleep), **jitter** (random offset 0..10% — full jitter по AWS — `random.uniform(0, min(cap, base*2^attempt))`), **don't retry on 4xx** except 429 (4xx — caller mistake). Если multi-upstream — per-upstream policy с circuit-breaker state.

### Q31. «Что такое hedging?»
> Запустить 2 копии запроса, использовать тот, который вернулся первым, отменить второй. Полезно, когда tail latency важна (Google «Tail at Scale» paper). Минус — удвоенная нагрузка. В LLM-world — `hedged requests` if first slow. На моём проекте hedged request не implemented, но я бы рассмотрел для /botrate, если бы tail-latency SLA был tight.

### Q32. «Что такое priority escalation pattern, который у вас реализован?»
> Когда upstream говорит «сложно/превышение лимита» (LLM-Integration 429 на priority=`low`), мы ретраим тот же запрос с повышенным priority `low → normal → high` (`httpx_async.py:85-93`). Логика: low-priority quota exceeded — но если бизнес-запрос важен, повысить приоритетный бюджет. На `high` всё ещё 429 → fall back на другую модель (`httpx_async.py:215`). Это модель **graceful degradation** — prioritize + fallback. Negative side: в принципе priority escalation «проталкивает» за лимиты.

### Q33. «Как бы вы handle отказ сервиса (e.g., LLM-Integration down)?»
> 1) **Circuit breaker** — open после N consecutive failures на свежем window — fast-fail вместо retry×5×180s. 2) **Fallback** на secondary model, если основная недоступна (у меня уже — qwen3-30B → expert). 3) **Bulkhead** — изолировать pool коннектов LLM-Integration, не положить весь сервис. 4) **Graceful degradation** — для не-critical подзадач пропустить шаг и продолжить (у меня `prompts_loop.py` обрабатывает `UserError` последнего промпта raise, остальных continue + notify). 5) **Оповещение** — structured error to user + metrics в Kafka + alert в Grafana. 6) **Recovery** — half-open state CB, probe-запросы.

### Q34. «Что такое `uvloop` и зачем?»
> Альтернативная реализация event loop для asyncio на базе libuv (Node.js's loop). Быстрее CPython's default на I/O-heavy — ~2–4x на coroutine-heavy workloads. Use: `uvloop.install()` before `asyncio.run()`. **Рекомендуется в production** для FastAPI/aiohttp при high-throughput. Not portable на Windows. При входе на Linux servers — приемлемо. Я бы рассмотрел для сервиса с большим RPS, но обычно network — не bottleneck, upstream LLM-latency преобладает.

### Q35. «Что сделает FastAPI при unhandled exception в endpoint?»
> Default Starlette behaviour: catches `Exception`, returns `500 Internal Server Error` с generic plain text (in production mode) или traceback (in debug). Custom exception classes: register с `@app.add_exception_handler(MyException, handler)` → return `Response`. У меня `botrate_validation_exception_handler` для `RequestValidationError` (`app.py:80`). **Important**: middleware seeing exceptions — order matters; exception handler runs after `ExceptionMiddleware` (Starlette), который сам ловит `HTTPException` и `RequestValidationError`.

### Q36. «Расскажи про паттерн Producer/Consumer»
> Producer кладёт задачу в очередь (`asyncio.Queue`, `redis`, Kafka topic), Consumer (worker pool) берёт из очереди, обрабатывает. **Decouple rate-of-production от rate-of-consumption** — natural backpressure. У меня Kafka-metrics producer (`KafkaClient`), downstream-aggregation — separate consumer. **In-process** queue: `asyncio.Queue(maxsize=...)` bounded; producers await `put()` when full — backpressure. **Cross-process**: Redis (RQ), RabbitMQ, Celery, Kafka. Для agent tool calls (high QPS) — Kafka уже используется для metric-streaming.

### Q37. «Как улучшить `tasks_queue`?»
> Заменить `list` + non-atomic check на: 1) `asyncio.Lock()` вокруг check/insert (или `asyncio.Semaphore(1)`), 2) Redis distributed lock `lock:webhook:{task_id}` (across workers), 3) `asyncio.Queue(maxsize=...)` для overall backpressure, 4) Idempotency-Key pattern вместо dedup-by-id, hash content requests, storage в Redis 24h. На agent-tps pattern: `Idempotency-Key` header в MCP request, Redis `SETNX` storage.

### Q38. «Как вы относитесь к `asyncio.to_thread` vs running loop in thread pool?»
> `asyncio.to_thread(func, *args)` (3.9+) — запускает sync-функцию в default `ThreadPoolExecutor` (min(32, os.cpu_count()+4)), awaits Future. Удобно, generic — не нужно создавать pool вручную. Для tight control — свой `ThreadPoolExecutor(max_workers=8)` + `loop.run_in_executor(executor, func, *args)`. У меня `convert_to_async.py` использует `to_thread`. Минус: если много sync-blocking работы — `ThreadPoolExecutor` может saturate. Решение — per-case pool (e.g., separate для LDAP crypto).

### Q39. «`ContextVar` — как это работает и зачем?»
> `contextvars.ContextVar` — async-safe equivalent of `threading.local`. Каждый async-context (Task) имеет свой snapshot of contextvars; switch context на Task-границе — `logging_context` (`utils/logger.py:10`) — я устанавливаю корреляцию (task_id, source) per call и вижу её в логах из nested корутин. **Critical**: `threading.local` НЕ работает с asyncio (т.к. все корутины в одном треде). ContextVar — proper solution. Limitation: by default, spawned Tasks наследуют context на момент create (snapshot), не realtime. Explicit `.set()`/`.reset()` pattern (как `logging_context.set(...)` и `logging_context.reset(token)` — `prompts_loop.py:164,229`).

### Q40. «Что делать, если upstream возвращает huge response (e.g., 100MB)?»
> 1) Stream it (`httpx` async streaming, `httpx.AsyncClient().stream()`); iterate chunks через `async for chunk in response.aiter_bytes()`. 2) Cap headers/request — `Range` headers. 3) Aggressive timeout для streaming reads. 4) Backup — temp file via `aiofiles`, не загружать в memory. 5) Не пытаться `.json()` этого — OOM. Для agent tools: stream response как resource-link, не inline text.

---

# Блок 7. Вопросы, которые ты задаёшь интервьюеру

Выбери 3–4. Спрашивай естественно — показывает, что ты думал о role.

### Про MCP-глубину
1. «Какой transport сейчас используется — stdio (local agents) или Streamable HTTP (удалённый backend service)? Это greenfield или есть существующие MCP-integrations, на которые я буду наращивать?»
2. «Как handle'ится версионирование tool'ов, когда agent'ы реализованы независимо от backend? `tool@v1` в названии? additive changes only?»
3. «Используете ли вы tool annotations нового spec (`readOnlyHint`, `idempotentHint`)? Если да — как LLM их интерпретирует в Вашей практике?»

### Про коллаборацию
4. «Как выглядит collaboration model между AI-инженерами и integration-layer team? Агент пишется в LangGraph/LlamaIndex — мы предоставляем MCP catalog? Где sits boundary — agent reasoning vs backend reliability?»
5. «Основной сигнал для оперирования — usage agents as primary metric» (я из desc вижу это, но): есть ли dashboard или specific SLI для tool-call success rate, agent-driven retry rate?»

### Про ops
6. «On-call expectation — есть ли rotation? У меня SRE-фон 4 года, готов, но хотел бы понять формат.»
7. «Deploy — только EKS или гибрид? Вакансия упоминает AWS/Kubernetes (EKS); on-prem присутствует в fintech/risk-сегменте?»
8. «Terraform ownership — у integration-layer team свой Terraform-repo или инфра общая? Где я граничу с platform/infra-team?»

### Про культуру / рост
9. «Как команда относится к self-taught engineers с практическим опытом? Я жил в коде, но formal CS-foundation у меня partial — как это выглядит в вашей команде?» (мягко, если чувствуешь tension).
10. «Учитывая, что у меня нет прямого MCP-опыта — какой онбординг ожидается? Pair-design с AI-engineer, док specs, sandbox cluster?»

---

# Блок 8. Тестирование (honest)

> Главный посыл: формального CI-gate для тестов у меня нет, запускал локально перед deploy. Но правильные паттерны (pytest fixtures, AsyncMock, `@patch`, data-driven cases, AAA) я знаю и применяю — ровно в той области, где это дёшево и быстро окупается: pure-функции парсинга и метрик RAGAS. В остальном проект — heavily integration с корпоративными сервисами, и стратегия там smoke/handshake на реальном окружении + structured logging для post-mortem.

## 8.0. Самоаудит — что реально лежит в `tests/`

| Файл | Что это | pytest собирает? |
|---|---|---|
| `test_extract_json.py` (82) | **Unit-тест на pure-функцию** `_extract_json`, data-driven table-of-cases. Runner самописный (`def main()`), тривиально в `@pytest.mark.parametrize`. | Зависит от имени — да |
| `test_evaluate_llm_response.py` (243) | **Правильные pytest unit-тесты** на `evaluate_llm_response`. `@pytest.fixture`, `@pytest.mark.asyncio`, `@patch`, `AsyncMock`, реальные `assert`. Внешние RAGAS-классы замоканы. | Да |
| `test_faithfulness.py` (140) | Тот же стиль: fixtures + `AsyncMock` для `evaluate_faithfulness`. | Да |
| `test_handle_no_prompts_found.py` (167) | **Component-чек** функции `app._handle_no_prompts_found` на JSON-fixture из `tests/data/`. Есть `assert`, но обёрнут в `try/except` со `print` — pytest-asyncio skip без маркера. | Скипнется (нет `@pytest.mark.asyncio`) |
| `test.py` (1555) | **Smoke exploration harness**. ~12 `async def test_xxx` функций (`test_vault_get`, `test_minerva`, `test_botrate`, `test_jhub` …), дёргают реальные корпоративные сервисы. Финал: `if __name__ == "__main__": asyncio.run(main_test())`. | Скипнется + нельзя в CI (нужен Vault/AD/LLM-IS токен) |
| `test_llm_limits_monitor.py` (17) | Smoke-runner на live job `check_llm_limits`. | Скипнется |

**Вывод:** «реальный» pytest-набор, который собирается детерминированно — это RAGAS-метрики + JSON-парсер. Остальное — exploration scripts, которые я запускал руками во время разработки каждого клиента на реальном окружении. Это честно и интенционально: разработка каждого из 11 клиентов шла через live handshake.

## 8.1. Уровни тестов и термины (с привязкой к моему коду)

**Пирамида тестов (Test Pyramid):** внизу — много дешёвых unit; середина — component/integration; верх — мало дорогих E2E. У меня фактически **diamond** (перевёрнутая пирамида): много exploration-скриптов против реальных сервисов, мало unit-тестов. Это осознанный выбор (из-за heavy внешних зависимостей), но в platform-layer я бы сместил needle в сторону пирамиды.

**Уровни:**
- **Unit** — одна функция/класс в изоляции, все зависимости замоканы. Мой пример: `test_extract_json.py` (pure-функция без зависимостей).
- **Component** — несколько модулей вместе, мокаются только границы. Мой пример: `test_handle_no_prompts_found.py` (функция `app.py` + Pydantic-модели + fixture JSON).
- **Integration** — несколько сервисов/баз вместе. У меня формально нет, потому что integration = live corporate env.
- **Smoke** — «живой?» — один сценарий end-to-end на реальном окружении. Мой пример: `test.py::test_vault_get`, `test.py::test_minerva`.
- **E2E (end-to-end)** — пользовательский путь через всё. У меня — absent; Pyrus → webhook → agents → post — это critical E2E-путь, который я тестирую вручную плюс RAGAS online eval в проде.
- **Contract** — consumer/provider договор о schema. У меня absent → improvement (Pact, см. блок 4.4).

**Mock types (xUnit patterns):**
- **Dummy** — объект передаётся, но не используется (заполнитель сигнатуры).
- **Stub** — возвращает предзаготовленный ответ на вызовы (state verification). У меня: `test_evaluate_llm_response.py:48-58` `groundedness_metric = Mock(); groundedness_metric.ascore = AsyncMock(return_value=Mock(value=0.9, ...))` — это stub.
- **Mock** — stub + records calls, допускает `assert_called_once()`. У меня `test_evaluate_llm_response.py:85-88` — state + behaviour verification одновременно.
- **Fake** — работающая, но упрощённая реализация (in-memory SQLite вместо Postgres). У меня нет — все упрощения идут через Mock.
- **Spy** — records calls без изменения поведения. Намёк в `assert_awaited_once()`.

**`Mock` vs `AsyncMock`:** `Mock` — для sync-объектов. Метод-корутина на обычном `Mock()` вернёт Mock, а не корутину — `await` упадёт. `AsyncMock` делает метод async, возвращает awaitable. У меня `groundedness_metric.ascore` — это async-метод RAGAS-метрики, поэтому `AsyncMock` (`test_evaluate_llm_response.py:49`). На класс-уровне — `Mock()` (т.к. класс не async), но его async-атрибуты — `AsyncMock`.

**`@patch("module.path.attr")`** — правило: патчу **там где импортируется**, не там где определено. У меня `@patch("metrics.ragas.evaluate_llm_response.ResponseGroundedness")` (`test_evaluate_llm_response.py:62`) — патчит имя в namespace `evaluate_llm_response`, куда класс импортирован, а не оригинальный `metrics.ragas.groundedness.ResponseGroundedness`. Это распространённая ошибка — патчить исходник, не consumer-name — патч «не сработает».

**AAA (Arrange-Act-Assert):** структура теста — подготовка, действие, проверка. У меня `test_evaluate_llm_response.py:71-88` — Arrange: setup mocks (71-73), Act: вызов `evaluate_llm_response(...)` (75-83), Assert: `assert_called_once()` + `assert_awaited_once()` (85-88).

**`@pytest.fixture`** — функция, возвращающая подготовленное состояние, ре-используемая между тестами. Scope: `function` (default, fresh per test), `module`, `session`. У меня `config` (`test_evaluate_llm_response.py:28-37`) и `mock_metrics` (`:45-58`). `llm_integration` (`:40-42`) — простейший.

**`@pytest.mark.parametrize`** — data-driven tests, одна функция генерирует N кейсов. Идиоматично заменяет мой `TEST_CASES = [...]` цикл в `test_extract_json.py:23-54, 62-78`. Пример переименования:

```python
@pytest.mark.parametrize("input_text, expected", [
    ('{"statements": ["a", "b"]}', {"statements": ["a", "b"]}),
    ('```json\n{"statements": ["a", "b"]}\n```', {"statements": ["a", "b"]}),
    ('not json', None),
])
def test_extract_json(input_text, expected):
    assert _extract_json(input_text) == expected
```

**`pytest-asyncio` strict vs auto mode:** `strict` (default, у меня) — каждый async-test должен нести `@pytest.mark.asyncio`. `auto` — все async-функции автоматически становятся async-testами, ничего помечать не надо. Включается через `asyncio_mode = "auto"` в `[tool.pytest.ini_options]`. **Это одно из моих improvement-действий** — сэкономило бы пометку и сняло скипы.

**Golden file / snapshot:** тест сравнивает результат с эталонным файлом/структурой. У меня фактически присутствует в зародыше — `tests/data/single_task_*.json` это golden Pyrus-вебхуки, `test_handle_no_prompts_found.py:19-20` их читает. Закончил бы через `pytest --snapshot-update` (syrupy/pytest-snapshot).

**Flaky test** — тест, который иногда падается без изменения кода: race, network, time-dependent. Классический кейс — `test_evaluate_llm_response_timeout` (`:187`) с `asyncio.sleep(10)` под `timeout=0.01` — на CI под нагрузкой может timing-попасть. Решение: `@pytest.mark.flaky` (pytest-rerunfailures) или mock часы (`freezegun`).

**Coverage** — `% строк/веток, исполненных тестами`. `pytest-cov`: `pytest --cov=utils --cov=clients --cov-report=term-missing --cov-fail-under=60`. Gate в CI: если ниже порога — fail. У меня coverage не измерялся — improvement.

## 8.2. Q&A — 12 вопросов про тестирование

### Q1. «Как вы тестируете приложение?»
> Слоисто. **Pure-функции и метрики** (`_extract_json`, `evaluate_llm_response`, `evaluate_faithfulness`) — proper pytest unit-тесты с fixtures, AsyncMock, patch-ем внешних RAGAS-классов, реальными `assert`. Это дёшево и быстро. **App-уровневые функции** (`_handle_no_prompts_found`) — component-тесты на JSON-fixture из `tests/data/`. **Внешние клиенты** (Pyrus, Confluence, Vault, LLM-Integration, AD) — для каждого я писал exploration-скрипт против реального корпоративного env во время разработки; формально они в `test.py`, не pytest-style, но идея — live handshake: «клиент реально ходит в сервис и возвращает shape, который я ожидаю». **E2E-путь** (Pyrus → webhook → agents → post в Pyrus) — пока тестирую вручную, плюс RAGAS online eval в проде даёт continuously faithfulness/groundedness скоринг каждого ответа. **Чего не хватает** — formal CI-gate (запускал локально перед deploy), contract-тестов на boundary agent → client, генерации недетерминированных Pyrus event-fixture-ов. Готов поднять CI-gate на pytest в первый месяц.

### Q2. «Какое у вас покрытие тестами?»
> Честно — coverage не измерял формально. Зная структуру: unit-тестами покрыты ~3 модуля (`_extract_json`, `evaluate_llm_response`, `evaluate_faithfulness`) — это <10% LOC, но **критичная** часть (парсинг LLM-вывода и метрики качества). Остальное — heavily integration с корпоративными сервисами, что мешает забежать в unit-без mock-инфраструктуры. В первый месяц я бы: (1) добавил `pytest-cov`, поставил `--cov-fail-under=60` как first step, (2) построил `conftest.py` с общими fixtures на `httpx.MockTransport` (см. Q6), что позволило бы unit-тестировать **все 11 клиентов** просто предоставив mock-handler, (3) поднял порог до 70-80% за квартал.

### Q3. «Как тестируете async/LLM-код?»
> `pytest-asyncio` в режиме strict — каждый async-test помечен `@pytest.mark.asyncio` (`test_evaluate_llm_response.py:61`). Внутри: `AsyncMock` для async-методов (`ascore = AsyncMock(return_value=Mock(value=0.9))`), обычные `Mock` для классов/атрибутов. Verification — `assert_awaited_once()` + `assert_called_once()` (`:85-88`), assert kwargs через `call_args.kwargs` (`:91-96`). Для timeout-handling — патчу таймаут на 0.01 и `AsyncMock(side_effect=slow_ascore)` с `asyncio.sleep(10)` (`:187-214`) — проверяю, что функция не пробрасывает exception наружу при timeout. Для LLM-недоступности — `AsyncMock(side_effect=RuntimeError("LLM упал"))` (`:227`), assert что `evaluate_llm_response` не raises, даже если оба metric-класса падают.

### Q4. «Mock vs stub разница?»
> Stub — отвечает на вызовы предзаготовленными значениями, для state-verification («что вернулось?»). Mock — stub + records calls, для behavior-verification («как вызывался?»). У меня в `test_evaluate_llm_response.py:48-58` технически stub — я делаю конфиг-возвр-значения. Дальше (`:85-88`) тот же объект используется как mock — `assert_called_once()` проверяет поведение. Поэтому в современных терминах разница скорее в **векторе verification**: assert-state → stub-usage; assert-behaviour → mock-usage. Fake — работающая упрощённая реализация (SQLite-in-memory); Spy — records без вмешательства.

### Q5. «TDD или тестирование после?»
> После, для этой задачи. Мой флоу: пишу функцию/клиента → пишу exploration-скрипт в `test.py` против реального env → проверяю shape → для pure-функций (json-парсер, метрики) пишу pytest-тесты рядом, обычно после. TDD я понимаю и практикую для случаев, где спека строгая: пишу параметризованный тест с ожидаемыми ветками first, потом реализацию. На этой роли (platform layer с MCP specs, у которых есть JSONSchema input) я бы чаще шёл TDD — schema уже описание контракта.

### Q6. «Как тестировать внешний API?»
> Pattern, который я бы применил к моему `AsyncHTTPClient` (`utils/httpx_async.py:12`) — `httpx.MockTransport`. `httpx.AsyncClient` принимает `transport=` аргумент; `MockTransport` — callable `[request] → response`. Идея: вместо мокания `httpx.AsyncClient` целиком, я передаю real client с mock-транспортом и проверяю **retry/backoff/429-escalation** логику моего `request()` (`httpx_async.py:29-249`) на синтетических responses. Это даёт real-coverage бизнес-логики (попыток, priority-эскалации на 429, fallback к expert - всё из `httpx_async.py`), без хождения в сеть. Альтернативы — `responses`/`respx` (test-only httpx-mocking libs), но `MockTransport` встроен в httpx и достаточен. Для каждого клиента в `conftest.py` — fixture `pyrus_client` с преднастроенным `MockTransport`.

### Q7. «Flaky tests?»
> Три источника: (1) **timing** — setTimeout, sleep на CI под нагрузкой; у меня риск — `test_evaluate_llm_response_timeout` (`:187`) с `asyncio.sleep(10)` под `timeout=0.01`; mitigation — `freezegun` для часов или `pytest-rerunfailures`. (2) **Race/shared state** — module-level mutable (`config`, `tasks_queue`); у меня `tasks_queue` в `app.py` — если два теста в одном process бегут, состояние протекает; mitigation — fixture per-test, cleanup. (3) **Network** — внешние вызовы в unit-тестах; у меня только в `test.py` exploration scripts, они в CI не побегут, но pytest их skip-нёт с warning о `@pytest.mark.asyncio` — это шум; mitigation — марк `@pytest.mark.live` + `pytest -m "not live"` по умолчанию.

### Q8. «Contract testing?»
> У меня отсутствует — improvement. Bridge к блоку 4.4: для platform-layer (MCP tools для агентов) consumer-driven contracts критичны — несколько consumer-агентов договариваются с моим integration-layer о том, что `tool_x` возвращает `KHubResult`-shape. Pact-style: consumer-тест блочит релиз provider-а, если schema изменилась. Для MCP это особенно ценно, потому что LLM-агенты получают schema через `tools/list` — сломать её = сломать reasoning.

### Q9. «Test pyramid как выглядит у вас?»
> Честно — **diamond**: много exploration scripts против реальных сервисов (`test.py`, 1555 строк), мало proper unit (3 файла). Это следствие проекта: heavy enterprise integration, где unit-тестировать клиента без mock-инфраструктуры — значит просто переписывать httpx-логику. **В первом месяце на этой роли** я бы построил `conftest.py` с `httpx.MockTransport`-fixture на каждый клиент, что сняло бы это ограничение и позволило сместить needle в сторону пирамиды: больше unit на уровне клиентов (retry, 429-эскалация, fallback), меньше live handshake.

### Q10. «Запуск тестов в CI?»
> Честно — не было formal CI-gate для тестов; запускал `uv run pytest tests/` локально перед commit/deploy. CI — GitLab, но trigger — build/deploy образа. **Что бы я сделал:** `.gitlab-ci.yml` stage `test` → `uv sync --extra dev && uv run pytest --cov=utils --cov=clients --cov-report=xml --cov-fail-under=60 --junitxml=report.xml`; artifacts: coverage + junit; merge-request gate blocking. Py cobertura-плагин для MR-отображения diff-coverage.

### Q11. «Как тестируете идемпотентность / race conditions?»
> Идемпотентность — эндпоинт `/webhook_handler` с `tasks_queue`-дедуп по `task_id` (`app.py`). Тест: отправляю два вебхука на один `task_id` подряд → assert только один дошёл до `process_selected_prompt`, второй скипнулся. Race conditions — это in-process и **не cross-process safe** (модуль-level `tasks_queue`, персистентности нет). Improvement должен быть Redis- backed (`SETNX idempotency:{tool}:{key}`), и тестировать через `pytest-asyncio` с двумя параллельными `asyncio.gather` запросами — assert одного выполнения. Для formal concurrency-тестов — `hypothesis` property-based.

### Q12. «Как тестируете LangGraph-агентов?»
> В моём проекте — пока только manual E2E: подбираю репрезентативный Pyrus event, сохраняю как golden (`tests/data/single_task_*.json`), запускаю `process_selected_prompt` вручную, сравниваю результат с ожидаемым по бизнес-логике. **Improvement на этой роли** — (1) snapshot/golden tests через `pytest-snapshot`: переиграть agent на фиксированном event, замокать LLM-call через `AsyncMock` с предзаписанным ответом, assert что output state и emitted tool calls совпадают с golden. (2) Property-based проверка reducer'а `Annotated[list, operator.add]` (`prisma_agent.py:66`) — два узла возвращают списки, assert аккумулятор равен конкатенации. (3) Для LLM-stochasticity — fixed seed (если поддерживается) или mocking LLM через общий fixture, чтобы тест был детерминированным.

## 8.3. Что бы улучшил на этой роли — gap pitches

1. **`asyncio_mode = "auto"` в `[tool.pytest.ini_options]`** в `pyproject.toml`. Снимает необходимость `@pytest.mark.asyncio` на каждом async-тесте и убирает skip-ы exploration-скриптов, которые я помечу `@pytest.mark.live` и буду skip'ать по умолчанию.

2. **`conftest.py` с общими fixtures.** Сейчас `config` и `llm_integration` дублируются между двумя RAGAS test-файлами. Общим стал бы `tests/conftest.py`: `config`, `mock_transport`, per-client `pyrus_client`/`confl_client`/`llm_integration_client` с `httpx.MockTransport`.

3. **`httpx.MockTransport` per `AsyncHTTPClient` subclass.** Главная инвестиция — fixture, который конструирует real `AsyncHTTPClient` с mock-транспортом и handler-функтором, возвращающим синтетические `httpx.Response`. Это даст unit-coverage всей retry/429-эскалации/fallback логике `utils/httpx_async.py:29-249`.

4. **`@pytest.mark.parametrize` для `TEST_CASES`** (`test_extract_json.py`). Приведение к идиоматичному pytest-style, переход с самописного runner.

5. **Coverage gate в CI.** `pytest --cov --cov-fail-under=60` как старт, поднятие до 80% за квартал. `diff cobertura` в MR.

6. **Contract tests (Pact-style) на boundary agent → client.** Особенно важно в MCP-роли — schema tools = контракт с LLM-агентами.

7. **Golden-file тесты для Pyrus event-fixtures.** `pytest-snapshot` для deterministic переигрывания agent-ов на репрезентативных вебхуках, с замоканным LLM-call.

8. **`assert` вместо `print("...OK")`** в `test_handle_no_prompts_found.py`. Сейчас там `try/except + print`, что прячет real failures — pytest-markup с `assert`-ом даёт proper red/green.

## 8.4. Bridge к Блоку 5 (honesty)

«Формального CI pipeline для тестов не было. Запускал `uv run pytest tests/` локально перед deploy; exploration scripts в `test.py` — руками на реальном env. По правильным паттернам (fixtures, AsyncMock, patch, parametrize, AAA) я понимаю и умею — ровно на той области, где это дёшево: pure-функции и метрики RAGAS. На MCP-integration role — где boundary = JSON-schema контракт с LLM-агентами — я вижу интеграцию CI-gate на pytest + coverage + contract tests как первый месяц».

---

## Финальные советы (субъективно)

1. **Главное — честность с уверенностью.** Когда не знаешь — говоришь: «Прямо не знаю, по аналогии с X...» затем best-effort. Это гораздо ценнее, чем блеф. Опытные интервьюеры замечают блеф мгновенно.

2. **Привязывай каждый ответ к `summarizer-it`.** Когда слышишь термин — сначала определение, **затем** «у меня это в `utils/httpx_async.py:32`» с конкретикой. Этого скорее всего не будет у кандидатов с большим формальным стажем.

3. **SRE-фон = твой козырь.** 4 года on-call, production-reliability-мышление — это senior-уровень, даже если формально Python-стаж меньше. Активно этим пользуйся.

4. **Не извиняйся за самоучку.** «Self-taught, products-of-their-hands, продуктово-инженерное мышление» — это ценится в startup-культуре. Ты не академик — ты shipped 5+ в продакшн. Это сильнее, чем диплом без shipped.

5. **MCP — важное слово в вакансии.** Прочти спеку ещё раз утром интервью. Запомни 2025-06-18 — дата свежей spec — name-dropping «последняя spec 2025-06-18 ...» signals, что ты реально изучил.

6. **Веди разговор двусторонним.** Если вопрос задан в общем — попроси «можете уточнить, в каком контексте?» — это не benefit, это правильно.

7. **Паузы.** Перед ответом = 1–2 сек. Не торопись. Senior отвечает размеренно.

8. **Если задают алго-задачу (не ожидается, но вдруг):** честно — «алгоритмы formal не решаю, но задачу обдумаю так: один/два подхода»; brute force + improving step. Они не ждут optimal DP от Python-application senior.

Удачи в понедельник. Код твой, все ответы укоренены в твоём реальном опыте.