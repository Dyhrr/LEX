"""Summarize locally synced emails."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path


EMAIL_FILE = Path("memory") / "emails.json"


class Command:
    description = "Summarize unread emails from a local mailbox."
    """Provide quick summaries of unread emails."""

    trigger = ["email_summary"]

    def __init__(self, context):
        self.context = context
        self.file = EMAIL_FILE

    # -----------------------------------------------------
    # Persistence helpers
    # -----------------------------------------------------
    def _load(self) -> list[dict]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return []

    def _save(self, data: list[dict]) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    # -----------------------------------------------------
    # Helper functions
    # -----------------------------------------------------
    def _categorize(self, subject: str) -> str:
        subj = subject.lower()
        if "invite" in subj or "meeting" in subj:
            return "invites"
        if "flight" in subj or "itinerary" in subj or "confirmation" in subj:
            return "flights"
        if "newsletter" in subj:
            return "newsletters"
        return "other"

    # -----------------------------------------------------
    # Command entry point
    # -----------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        emails = self._load()

        unread = [e for e in emails if e.get("unread", True)]

        if not tokens or tokens[0] == "summary":
            if not unread:
                return "[Lex] No new emails."
            counts = {"invites": 0, "flights": 0, "newsletters": 0, "other": 0}
            for e in unread:
                counts[self._categorize(e.get("subject", ""))] += 1
            parts = []
            if counts["invites"]:
                parts.append(
                    f"{counts['invites']} meeting invite{'s' if counts['invites'] != 1 else ''}"
                )
            if counts["flights"]:
                parts.append(
                    f"{counts['flights']} flight confirmation{'s' if counts['flights'] != 1 else ''}"
                )
            if counts["newsletters"]:
                parts.append(
                    f"{counts['newsletters']} newsletter{'s' if counts['newsletters'] != 1 else ''}"
                )
            if counts["other"]:
                parts.append(
                    f"{counts['other']} message{'s' if counts['other'] != 1 else ''}"
                )
            return "[Lex] You have " + ", ".join(parts) + "."

        if tokens[0] == "list":
            if not unread:
                return "[Lex] No unread emails."
            return "\n".join(
                f"{i+1}. {e.get('subject', '(no subject)')}" for i, e in enumerate(unread)
            )

        if tokens[0] == "read" and len(tokens) >= 2:
            try:
                idx = int(tokens[1]) - 1
            except ValueError:
                return "[Lex] Give me a valid number."
            if 0 <= idx < len(unread):
                email = unread[idx]
                email["unread"] = False
                self._save(emails)
                body = email.get("body", "").strip().splitlines()
                snippet = body[0] if body else "(no content)"
                return f"[Lex] From {email.get('from', 'unknown')}: {snippet}"
            return "[Lex] No email with that number."

        if tokens[0] == "action":
            actionable = [e for e in unread if self._categorize(e.get("subject", "")) != "newsletters"]
            if not actionable:
                return "[Lex] Nothing needs action."
            top = actionable[0]
            return f"[Lex] {top.get('subject', '(no subject)')} from {top.get('from', 'unknown')} seems important."

        return "[Lex] Use 'email_summary', 'list', 'read <num>' or 'action'."

