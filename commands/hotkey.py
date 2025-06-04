import asyncio


class Command:
    trigger = ["hotkey"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        return "[Lex] TODO: hotkey feature"
