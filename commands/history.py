"""Show recent command history and results."""

import asyncio


class Command:
    description = "Show recent command history and results."
    """Show recent command history and results."""

    trigger = ["history", "context"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        history: list[tuple[str, str]] = self.context.get("history", [])
        if not history:
            return "[Lex] No recent history."
        lines = []
        for i, (cmd, resp) in enumerate(history[-5:], start=1):
            lines.append(f"{i}. > {cmd} | {resp}")
        return "\n".join(lines)
