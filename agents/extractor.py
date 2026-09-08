"""Extractor node: uses Claude to turn each raw email into a structured Application record."""

import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from state import AgentState

llm = ChatOpenAI(
    model="gpt-5.6-luna",
)

EXTRACT_PROMPT = SystemMessage(
    content="""You extract structured job-application data from \
an email's subject, sender, and snippet.

Return ONLY a JSON object with these fields:
- "is_job_related": true/false — is this actually about a job application?
- "company": the hiring company's name, or "" if unclear
- "role": the job title, or "" if unclear
- "stage": one of "applied", "interview", "offer", "rejected", "unknown"

If is_job_related is false, leave the other fields empty/unknown. Respond with JSON only, \
no other text."""
)


def _extract_one(email: dict) -> dict | None:
    content = (
        f"Subject: {email['subject']}\n"
        f"From: {email['sender']}\n"
        f"Date: {email['date']}\n"
        f"Snippet: {email['snippet']}"
    )
    response = llm.invoke([EXTRACT_PROMPT, HumanMessage(content=content)])

    try:
        data = json.loads(response.content)
    except json.JSONDecodeError:
        return None

    if not data.get("is_job_related"):
        return None

    return {
        "email_id": email["id"],
        "company": data.get("company", "") or "Unknown",
        "role": data.get("role", "") or "Unknown",
        "stage": data.get("stage", "unknown"),
        "date": email["date"],
    }


def extractor_node(state: AgentState) -> dict:
    applications = []
    for email in state["raw_emails"]:
        record = _extract_one(email)
        if record:
            applications.append(record)

    return {"applications": applications}
