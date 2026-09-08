# Job Application Tracker Agent

An asynchronous LangGraph pipeline that searches Gmail for recent job-application
messages, extracts structured application details with an OpenAI chat model, and
stores new records in a local CSV file.

The pipeline is intentionally small and has three nodes:

1. **Scanner** - calls the configured Gmail MCP server and parses matching email
   metadata.
2. **Extractor** - classifies each email and extracts the company, role, stage,
   and date.
3. **Tracker** - appends only previously unseen applications to
   `data/tracker.csv`, using the Gmail email ID for deduplication.

## Requirements

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Node.js and `npx` (required by the Gmail MCP server)
- A Gmail MCP server that exposes a `search_emails` tool
- An OpenAI API key

## Setup

Install the project dependencies:

```bash
uv sync
```

Create a local `.env` file with the credentials needed by the model and Gmail
MCP server. Do not commit this file:

```dotenv
OPENAI_API_KEY=your-openai-api-key
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-oauth-client-secret
```

The default `mcp_config.json` starts the Gmail MCP server through `npx`:

```json
{
  "gmail": {
    "command": "npx",
    "args": ["-y", "@artymclabin/gmail-mcp"],
    "transport": "stdio"
  }
}
```

Complete the Gmail MCP server's OAuth setup according to that server's
documentation before running the agent. Authentication tokens and local
credentials must remain outside version control.

## Run

Run one scan from the repository root:

```bash
uv run python main.py
```

The scanner uses this default Gmail query when no query is supplied:

```text
subject:(application OR interview OR offer OR "not moving forward" OR rejected OR "thank you for applying") newer_than:30d
```

The command prints the available Gmail MCP tools and a run summary. Results are
written to `data/tracker.csv`. Re-running the command does not add an email
whose `email_id` is already present.

## Tracker format

`data/tracker.csv` contains these columns:

| Column | Description |
| --- | --- |
| `email_id` | Gmail message identifier used for deduplication |
| `company` | Hiring company, or `Unknown` when it cannot be inferred |
| `role` | Job title, or `Unknown` when it cannot be inferred |
| `stage` | `applied`, `interview`, `offer`, `rejected`, or `unknown` |
| `date` | Date reported by Gmail |

## Project layout

```text
.
├── agents/
│   ├── scanner.py       # Gmail MCP search and response parsing
│   ├── extractor.py     # OpenAI structured extraction
│   └── tracker.py       # CSV persistence and deduplication
├── data/tracker.csv     # Local application data
├── graph.py             # LangGraph node wiring
├── main.py              # Async application entrypoint
├── mcp_config.json      # Gmail MCP server configuration
├── state.py             # Shared TypedDict state and record types
└── pyproject.toml       # Project and dependency metadata
```

## Development

Run the available static checks and tests:

```bash
uv run ruff check .
uv run pytest
```

The repository currently has no automated test cases, so changes to parsing,
extraction, or CSV behavior should be manually exercised with representative
MCP responses and a disposable tracker file.

## Current limitations and roadmap

- The scanner depends on the Gmail MCP server's text response format and only
  parses message metadata returned in the expected `ID`, `Subject`, `From`, and
  `Date` layout.
- Email snippets are currently empty because `search_emails` does not provide
  them; the extractor therefore has limited message content.
- The tracker records new applications but does not update an existing row when
  an application's stage changes.
- CSV is the current storage backend. A future version may use Google Sheets or
  Notion through MCP.
- A future stage-change detector could notify through Slack or another MCP
  integration.
- A small hand-labeled evaluation set should be added to measure extraction
  accuracy.
