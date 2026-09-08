# Job Application Tracker Agent

Scans Gmail for job-application-related emails, extracts structured data (company, role,
stage) with Claude, and maintains a deduplicated CSV tracker — via a real Gmail MCP server.

## Setup

    uv sync
    cp .env.example .env   # add ANTHROPIC_API_KEY

Set up the Gmail MCP server's OAuth (one-time — see its README):

    npx -y @gongrzhe/server-gmail-autoauth-mcp auth

## Run

    uv run python main.py

Output goes to `data/tracker.csv`. Re-running only adds genuinely new emails — already-tracked
ones are skipped by `email_id`.

## Roadmap
- [x] Day 1-2: MCP-connected scanner -> LLM extractor -> CSV tracker pipeline
- [ ] Day 3: swap CSV for Google Sheets MCP server, or Notion MCP server
- [ ] Day 4: add a "stage change" detector — diff against previous run, notify on updates
      (e.g. Slack MCP message when an application moves from "applied" to "interview")
- [ ] Day 5: small eval set — hand-label 15-20 real emails, measure extraction accuracy