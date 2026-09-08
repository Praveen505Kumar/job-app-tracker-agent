"""Shared state schema. Lists use operator.add so each node appends instead of overwriting."""

import operator
from typing import Annotated, TypedDict


class EmailSummary(TypedDict):
    id: str
    sender: str
    subject: str
    date: str
    snippet: str


class Application(TypedDict):
    email_id: str
    company: str
    role: str
    stage: str  # applied | interview | offer | rejected | unknown
    date: str


class AgentState(TypedDict):
    query: str  # search query used against Gmail
    raw_emails: list[EmailSummary]  # from scanner node
    applications: Annotated[list[Application], operator.add]  # accumulated by extractor
    new_rows_written: int  # from tracker node
    summary: str  # from notifier-style final step
