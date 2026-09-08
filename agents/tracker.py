"""Tracker node: appends new application records to a local CSV, deduplicating by email_id."""

import csv
import os

from state import AgentState

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tracker.csv")
FIELDNAMES = ["email_id", "company", "role", "stage", "date"]


def _load_seen_ids() -> set[str]:
    if not os.path.exists(CSV_PATH):
        return set()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return {row["email_id"] for row in csv.DictReader(f)}


def tracker_node(state: AgentState) -> dict:
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    seen_ids = _load_seen_ids()

    new_rows = [a for a in state["applications"] if a["email_id"] not in seen_ids]

    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_rows)

    summary = (
        f"Scanned {len(state['raw_emails'])} emails, found {len(state['applications'])} "
        f"job-related, added {len(new_rows)} new rows to tracker.csv "
        f"({len(state['applications']) - len(new_rows)} already tracked)."
    )

    return {"new_rows_written": len(new_rows), "summary": summary}
