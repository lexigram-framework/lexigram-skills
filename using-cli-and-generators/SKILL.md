---
name: using-cli-and-generators
description: Use when running lexigram CLI commands, scaffolding new packages or code, or adding CLI command groups
---

# Using CLI and Generators

## Overview

The `lexigram` CLI provides 73 commands across 24 packages, including 42 code generators for scaffolding new components. Commands are organized into groups via typer and support dynamic contribution via entry points.

## Quick Reference

### Project Setup

```bash
lexigram new project my-app        # Create new project
lexigram new package my-package    # Scaffold extension package
lexigram init                      # Init in existing project
```

### Code Generators (42 total)

```bash
lexigram gen list                  # List all generators

lexigram gen model <name>          # SQLAlchemy model
lexigram gen repository <name>     # DB repository with queries
lexigram gen service <name>        # Service with unit of work
lexigram gen controller <name>     # Web controller with routes
lexigram gen resource <name>       # RESTful CRUD resource
lexigram gen graphql <name>        # GraphQL schema + resolvers
lexigram gen middleware <name>     # Web middleware
lexigram gen provider <name>       # DI provider
lexigram gen module <name>         # Module definition
lexigram gen test <name>           # Test scaffold

lexigram gen mcp-server <name>     # MCP server script
lexigram gen mcp-controller <name> # MCP controller class
lexigram gen workflow_def <name>   # Workflow definition
lexigram gen saga <name>           # Saga orchestrator
lexigram gen event_handler <name>  # Event handler
lexigram gen task <name>           # Background task
lexigram gen api_client <name>     # External API client
lexigram gen cache_repo <name>     # Cache-backed repository
```

### Database

```bash
lexigram db init                   # Init migrations
lexigram db migrate "message"      # Generate migration
lexigram db upgrade                # Apply pending
lexigram db downgrade              # Revert
lexigram db seed                   # Seed data
lexigram db reset                  # Drop + recreate
lexigram db shell                  # Database shell
lexigram db inspect                # Show schema
lexigram db backup / restore       # Backup/restore
lexigram db status / history       # Migration state
```

### Configuration

```bash
lexigram config show               # Current config
lexigram config validate           # Validate config
lexigram config doctor             # Diagnose issues
lexigram config env                # Show env vars used
lexigram config diff <file1> <file2>
lexigram config env-example        # Generate .env.example
lexigram config schema             # Export JSON schema
```

### Inspection

```bash
lexigram inspect providers         # Registered providers
lexigram inspect routes            # HTTP routes
lexigram inspect container         # DI container state
lexigram inspect events            # Event handlers
lexigram inspect tasks             # Task handlers
lexigram inspect dependencies      # Provider deps graph
lexigram inspect modules           # Registered modules
lexigram inspect health            # Provider health status
```

### Project Checks

```bash
lexigram project test              # Run tests
lexigram project lint              # Run linter
lexigram project typecheck         # Run mypy
lexigram project routes            # List all routes
lexigram project run-all           # Full check suite
lexigram project deps              # Audit dependencies
```

### System

```bash
lexigram system info               # Environment info
lexigram system health             # Project health
lexigram system doctor             # Diagnose system
lexigram system providers          # List providers
```

### Contributed Groups

24 contributed groups from extension packages:

```bash
lexigram admin    lexigram ai          lexigram audit
lexigram auth     lexigram cache       lexigram events
lexigram features lexigram mcp         lexigram monitor
lexigram nosql    lexigram notification lexigram queue
lexigram search   lexigram sql         lexigram storage
lexigram tasks    lexigram tenancy     lexigram vector
lexigram web      lexigram workflow
```

## Adding a CLI Command

```python
# lexigram-cli/src/lexigram/cli/commands/mycmd.py
import typer
from lexigram.cli.runtime import handle_errors
from lexigram.cli.output import OutputManager

app = typer.Typer(name="mycmd")

@app.command()
@handle_errors
def my_action(
    name: str = typer.Argument(..., help="Thing name"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Do something with name."""
    out = OutputManager()
    out.info(f"Processing {name}")
```

Register in `runtime/main.py`:
```python
from lexigram.cli.commands import mycmd
app.add_typer(mycmd.app, name="mycmd", help="My commands")
```

For contributed commands from extension packages, implement `CliContributorProtocol` and register via `[project.entry-points."lexigram.cli.contributors"]`.

## Common Mistakes

- Using `lexigram gen` without an active project — generators need project context
- Forgetting to register new command modules in `runtime/main.py`
- Not using `@handle_errors` decorator — raw exceptions leak to user
- Running `db upgrade` without `db init` first
- Running commands outside project root — CLI discovers config from cwd
