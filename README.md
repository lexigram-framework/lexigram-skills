# Lexigram Skills

Opencode skills for the [Lexigram framework](https://github.com/lexigram-framework/lexigram-dev) — an async-first, contract-based Python application platform.

## Installation

Add to your project's `opencode.json`:

```json
{
  "plugin": ["lexigram-skills@git+https://github.com/lexigram-framework/lexigram-skills.git"]
}
```

Or install globally in `~/.config/opencode/opencode.json`. Restart opencode, then skills are discoverable via the `skill` tool.

## Skills

### AI

| Skill | Description |
|-------|-------------|
| `ai-subsystem-quickstart` | LLM clients, RAG pipelines, agents, memory, MCP servers |

### CLI

| Skill | Description |
|-------|-------------|
| `cli-project-scaffolding` | Creating projects, packages, init config |
| `cli-code-generation` | 42 code generators — models, services, controllers, and more |
| `cli-database-operations` | Migrations, seeding, backup/restore, schema inspection |
| `cli-config-and-inspect` | Configuration management, runtime inspection, diagnostics |

### Core Patterns

| Skill | Description |
|-------|-------------|
| `creating-providers-and-modules` | Providers, modules, DI container wiring |
| `configuration-management` | YAML config, env vars, profiles |
| `using-result-and-error-codes` | Result[T,E], LEX_ERR_* codes, exception hierarchy |

### Data

| Skill | Description |
|-------|-------------|
| `database-repository-pattern` | Async SQL, repositories, domain models, migrations |
| `caching-patterns` | Multi-backend caching, stampede protection |

### Web

| Skill | Description |
|-------|-------------|
| `web-controllers-and-routing` | HTTP controllers, middleware, guards |
| `events-and-messaging` | CQRS, event bus, queues, outbox |
| `resilience-patterns` | Retry, circuit breaker, bulkhead, rate limiting |

### Testing

| Skill | Description |
|-------|-------------|
| `testing-with-lexigram` | TestEnvironment, module stubs, fakes |

## Repositories

- [Lexigram Framework](https://github.com/lexigram-framework/lexigram-dev)
- [Lexigram Docs](https://github.com/lexigram-framework/lexigram-docs)
- [Lexigram Skills](https://github.com/lexigram-framework/lexigram-skills)
