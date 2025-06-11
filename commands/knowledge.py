"""Search local documentation for answers."""

import asyncio
from pathlib import Path


DOC_FILES = [Path("README.md"), Path("documentation.md"), Path("What they do")]


class Command:
    description = "Search local documentation for matching lines."
    """Simple knowledge base query from bundled docs."""

    trigger = ["knowledge"]

    def __init__(self, context):
        self.context = context
        self.files = [p for p in DOC_FILES if p.exists()]

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        query = args.strip().lower()
        if not query:
            return "[Lex] Ask me about something in the docs."

        matches: list[str] = []
        for file in self.files:
            try:
                with file.open("r", encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        if query in line.lower():
                            matches.append(f"{file.name}:{i}: {line.strip()}")
                            if len(matches) >= 3:
                                break
            except Exception:
                continue
            if len(matches) >= 3:
                break

        if not matches:
            return "[Lex] Nothing found."
        return "\n".join(matches)
