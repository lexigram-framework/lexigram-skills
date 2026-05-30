# Lexigram Skills

Opencode skills for the [Lexigram framework](https://github.com/lexigram-framework/lexigram-dev).

## Installation

Add to your project's `opencode.json`:

```json
{
  "plugin": ["lexigram-skills@git+https://github.com/lexigram-framework/lexigram-skills.git"]
}
```

Or install globally in `~/.config/opencode/opencode.json`.

## Skills

| Skill | Use when... |
|-------|-------------|
| `ai-subsystem-quickstart` | Setting up LLM, RAG, agents, memory, MCP |
| `caching-patterns` | Adding caching, configuring backends, preventing stampedes |
| `cli-code-generation` | Scaffolding code with the 42 generators |
| `cli-config-and-inspect` | Viewing config, inspecting runtime, diagnosing systems |
| `cli-database-operations` | Running migrations, seeding, backup/restore |
| `cli-project-scaffolding` | Creating projects, packages, init |
| `configuration-management` | Config, env vars, profiles, YAML |
| `creating-providers-and-modules` | Creating providers, modules, DI wiring |
| `database-repository-pattern` | Database access, repositories, domain models |
| `events-and-messaging` | CQRS, event bus, queues, outbox |
| `resilience-patterns` | Retry, circuit breaker, bulkhead, rate limiting |
| `testing-with-lexigram` | TestEnvironment, stubs, fakes |
| `using-result-and-error-codes` | Result[T,E], error codes, exception hierarchy |
| `web-controllers-and-routing` | HTTP endpoints, controllers, middleware, guards |
