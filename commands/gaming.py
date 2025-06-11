"""Roll dice or flip a coin."""

import asyncio
import random


class Command:
    description = "Roll dice or flip a coin."
    trigger = ["game", "gaming"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """Provide simple gaming utilities like dice rolls or coin flips."""
        command = args.strip().lower()
        await asyncio.sleep(0)  # allow context switch

        if command in {"roll", "dice"}:
            result = random.randint(1, 6)
            return f"[Lex] You rolled a {result}. Try not to waste it."

        if command in {"flip", "coin"}:
            result = "heads" if random.choice([True, False]) else "tails"
            return f"[Lex] The coin landed on {result}. Riveting, I know."

        return "[Lex] Try 'game roll' or 'game flip'. That's all I do for now."
