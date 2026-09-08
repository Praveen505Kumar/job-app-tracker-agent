"""Scanner node: calls the Gmail MCP server's search_emails tool and parses its text response."""

import re

from state import AgentState

DEFAULT_QUERY = (
    'subject:(application OR interview OR offer OR "not moving forward" OR '
    'rejected OR "thank you for applying") newer_than:30d'
)

# Each record looks like:
# ID: 1a057ae8cf72a3a4
# Subject: Your Labor Day offer came early
# From: Zach at Educative <zach.m@educative.io>
# Date: Mon, 31 Aug 2026 04:57:28 -0700
RECORD_PATTERN = re.compile(
    r"ID:\s*(?P<id>\S+)\s*\n"
    r"Subject:\s*(?P<subject>.*?)\s*\n"
    r"From:\s*(?P<sender>.*?)\s*\n"
    r"Date:\s*(?P<date>.*?)\s*(?=\n\n|\Z)",
    re.DOTALL,
)


def _extract_text(raw_result) -> str:
    """The MCP response is a list of content blocks; pull out the text field."""
    if isinstance(raw_result, str):
        return raw_result
    if isinstance(raw_result, list):
        return "\n".join(
            block.get("text", "") for block in raw_result if isinstance(block, dict)
        )
    return str(raw_result)


async def scanner_node(state: AgentState, mcp_tools: dict) -> dict:
    search_tool = mcp_tools["search_emails"]
    query = state.get("query") or DEFAULT_QUERY

    raw_result = await search_tool.ainvoke(
        {
            "query": query,
            "maxResults": 25,
        }
    )
    print(f"Raw MCP response for query '{query}':\n{raw_result}\n")

    text = _extract_text(raw_result)
    matches = RECORD_PATTERN.finditer(text)

    raw_emails = [
        {
            "id": m.group("id"),
            "sender": m.group("sender"),
            "subject": m.group("subject"),
            "date": m.group("date"),
            "snippet": "",  # not provided by search_emails; fetch via read_email if ever needed
        }
        for m in matches
    ]
    print(f"Found {len(raw_emails)} emails matching query '{query}'.")

    return {"raw_emails": raw_emails}
