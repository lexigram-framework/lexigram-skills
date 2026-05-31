# lexigram skills

*how Lexigram teaches the AI in your editor to build with it.*

These are skill files for AI coding agents — Claude Code, OpenCode, and friends. Drop them into your agent, and when you ask it to wire a provider, scaffold a controller, or set up RAG, the agent reaches for the same patterns you would.

> **important — this is not a python package.** `lexigram-skills` is not on PyPI. `uv add lexigram-skills` will 404. These are markdown files (`SKILL.md`) consumed by AI coding agents, not python imports. The framework you'd `pip install` is **[lexigram](https://github.com/lexigram-framework/lexigram)** — this repo only teaches your editor how to use it.

## install

For OpenCode, add to your project's `opencode.json`:

```json
{
  "plugin": ["lexigram-skills@git+https://github.com/lexigram-framework/lexigram-skills.git"]
}
```

Or install globally in `~/.config/opencode/opencode.json`. Restart the agent; skills become discoverable via the `skill` tool.

For Claude Code, point its skills directory at this repo, or copy the folders you want into `~/.claude/skills/`.

## what's in the box

### AI

| Skill | Use when… |
|-------|-----------|
| `ai-subsystem-quickstart` | Setting up llms, rag pipelines, agents, memory, or mcp servers |

### CLI

| Skill | Use when… |
|-------|-----------|
| `cli-project-scaffolding` | Creating projects, packages, init config |
| `cli-code-generation` | Scaffolding from one of the 42 generators — models, services, controllers, more |
| `cli-database-operations` | Running migrations, seeding, backup/restore, schema inspection |
| `cli-config-and-inspect` | Viewing config, inspecting runtime, diagnosing systems |

### Core patterns

| Skill | Use when… |
|-------|-----------|
| `creating-providers-and-modules` | Wiring providers, modules, and the DI container |
| `configuration-management` | YAML config, env vars, profiles |
| `using-result-and-error-codes` | `Result[T, E]`, `LEX_ERR_*` codes, exception hierarchy |

### Data

| Skill | Use when… |
|-------|-----------|
| `database-repository-pattern` | Async SQL, repositories, domain models, migrations |
| `caching-patterns` | Multi-backend caching, stampede protection |

### Web

| Skill | Use when… |
|-------|-----------|
| `web-controllers-and-routing` | HTTP controllers, middleware, guards |
| `events-and-messaging` | CQRS, event bus, queues, outbox |
| `resilience-patterns` | Retry, circuit breaker, bulkhead, rate limiting |

### Testing

| Skill | Use when… |
|-------|-----------|
| `testing-with-lexigram` | `TestEnvironment`, module stubs, fakes |

## how a skill works

Each skill is a single `SKILL.md` file with YAML frontmatter (`name`, `description`) and a body of code-led examples. When you ask your AI agent to do something matching a skill's description, the agent loads that file and follows it. No magic, no plugins to write — just markdown your editor reads.

A skill is roughly: one task, twelve to a hundred lines of example code, a quick-reference table, and a short list of common mistakes. Easy to read, easy to extend.

## early on purpose

These skills track Lexigram 0.1.x. The framework is still soft; the skills move with it. If a skill steers you wrong, [open an issue](https://github.com/lexigram-framework/lexigram-skills/issues) — that's how the next release gets better.

## known gaps

A few skills we know we owe — pull requests welcome:

- **SSE / real-time web patterns.** No skill yet covers HTMX + SSE + `EventChannel` end-to-end.
- **Shared-queue lifecycle.** `creating-providers-and-modules` doesn't yet walk through subscribe/unsubscribe patterns where multiple owners share a queue (a real foot-gun in production).
- **`lexigram-ui` skill.** Component behavior and CDN dependencies aren't documented as a skill yet.
- **CSP guidance in `web-controllers-and-routing`.** Content-security-policy configuration is missing.

If you've solved one of these and want to share the pattern, see [contributing](#contributing).

## contributing

A new skill is a new directory with a single `SKILL.md` inside. Frontmatter:

```yaml
---
name: your-skill-name
description: Use when …
---
```

Keep the body code-led. Lead with the "what you'd write" snippet, not prose. Each skill should answer one question and end with a quick-reference table.

## repositories

- [lexigram](https://github.com/lexigram-framework/lexigram) — the framework itself
- [lexigram-docs](https://github.com/lexigram-framework/lexigram-docs) — the docs site
- [lexigram-skills](https://github.com/lexigram-framework/lexigram-skills) — this repo

---

*made for people who like building things and keeping them buildable.*
