# Copilot Instructions

## Repository purpose

This repository is a small Python application that tracks job applications from
Gmail. It uses LangGraph to run three nodes in order:

```text
scanner -> extractor -> tracker
```

- `agents/scanner.py` calls the Gmail MCP server's `search_emails` tool and
  parses the server's text response.
- `agents/extractor.py` sends email metadata to an OpenAI chat model and
  produces `Application` records.
- `agents/tracker.py` appends new records to `data/tracker.csv` and deduplicates
  by `email_id`.
- `graph.py` wires the nodes together.
- `main.py` loads environment variables and `mcp_config.json`, creates the MCP
  client, and invokes the graph.
- `state.py` defines the shared LangGraph state and TypedDict record shapes.

## Working conventions

- Target Python 3.11 or newer.
- Use `uv` for dependency installation and command execution.
- Preserve the existing async flow in `main.py` and `scanner_node`.
- Keep the shared state types in `state.py` authoritative; update them when a
  record shape changes.
- Keep the pipeline nodes focused. Do not move Gmail access into the extractor
  or CSV persistence into the scanner.
- Reuse existing constants and helpers before adding new parsing or file I/O
  logic.
- Prefer explicit types, narrow error handling, and clear failures over silent
  fallbacks.
- Keep documentation and configuration examples consistent with the actual
  model provider and MCP server.

## Important behavior

- `scanner_node` uses `DEFAULT_QUERY` unless `state["query"]` is populated.
- The scanner expects records containing `ID`, `Subject`, `From`, and `Date`.
  Changes to the Gmail MCP server response format require coordinated parser
  updates and validation.
- The extractor must return JSON-compatible data matching the allowed stage
  values: `applied`, `interview`, `offer`, `rejected`, or `unknown`.
- `tracker_node` uses `email_id` as the stable deduplication key and writes
  `data/tracker.csv` with the columns `email_id`, `company`, `role`, `stage`, and
  `date`.
- Do not change existing tracker rows casually; local CSV data may represent
  real application history.

## Configuration and security

- Secrets belong in the ignored `.env` file or the user's environment, never in
  source code, documentation, tests, or commits.
- Do not expose API keys, OAuth client secrets, Gmail tokens, or email contents
  in logs or generated examples.
- `mcp_config.json` is the source of truth for the local Gmail MCP command.
  Keep OAuth/token files outside the repository.
- Be careful when running the agent: it reads real Gmail data and writes to the
  local tracker.

## Validation

After code changes, run the smallest relevant checks:

```bash
uv run ruff check .
uv run pytest
```

For scanner changes, also test representative MCP response text. For extractor
changes, test valid JSON, non-job emails, missing fields, and invalid model
output. For tracker changes, test an empty CSV, an existing CSV, and duplicate
email IDs without overwriting unrelated rows.

Do not add dependencies or test frameworks unless the task requires them.
Avoid unrelated refactors and do not modify generated virtual-environment files.
