import asyncio
from core import nlp


class Command:
    trigger = ["learn", "teach"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """Teach Lex new phrases or list learned phrases."""
        args = args.strip()
        if args == "list":
            custom = await asyncio.to_thread(nlp.get_custom_intents)
            if not custom:
                return "[Lex] I haven't learned anything yet."
            return "\n".join(f"{k} -> {v}" for k, v in custom.items())

        if " as " not in args:
            return "[Lex] Usage: learn <phrase> as <command>"

        phrase, command = args.split(" as ", 1)
        phrase = phrase.strip()
        command = command.strip()
        if not phrase or not command:
            return "[Lex] Usage: learn <phrase> as <command>"

        await asyncio.to_thread(nlp.add_custom_intent, phrase, command)
        return f"[Lex] Learned '{phrase}' -> '{command}'"

