# Senior Python Engineer — MCP Integration Layer

We are looking for a senior Python engineer to build the integration layer that lets our LLM agents act on real systems. You will own the backend service through which agentic products — chatbot and future agentic systems — invoke internal APIs across the company. The current transport protocol for this layer is MCP (Model Context Protocol).

You are going to work closely with our AI Engineers. They build agent logic; you build the reliable, ergonomic surface they call. The split lets each side focus: agent reasoning on one side, backend integrations and reliability on the other.

## Your Future Responsibilities Await

### Design and ship integrations that LLMs can use effectively

Design tool APIs with attention to schema clarity, error message quality, and idempotency — agents reason about your responses, so wording and structure matter

Own each integration end-to-end: auth, rate limiting, retries, safe defaults for destructive or sensitive operations, and observability

Write focused tests, including contract tests against the upstream services you integrate with

### Build the platform around the integrations

Define and evolve the internal template for adding new tools — the catalog will grow, and the second integration should be cheaper than the first

Instrument every tool with metrics, logs, and traces from day one; usage by agents is the primary signal we operate on

Package, deploy, and operate the service in AWS/Kubernetes (EKS)

## What we expect from the candidate

- Senior-level Python backend experience (5+ years), with services you have shipped, operated, and been on-call for
- Experience designing and operating microservices (FastAPI or similar)
- Hands-on experience with Docker and Kubernetes
- A platform mindset: your users are other engineers, and your API design reflects that

## Would be a big plus

- Prior work with LLM tool-calling / function-calling / agent frameworks (MCP, OpenAI/Anthropic tool use, LangChain, or similar) — or strong curiosity about this space
- Strong API design background: OpenAPI, contract testing, SDK ergonomics, schema evolution
- AWS and Terraform experience
- Understanding of concurrency models in Python (asyncio, multiprocessing, threading)
- Fintech, payments, or risk domain exposure
