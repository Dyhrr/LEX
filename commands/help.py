class Command:
    trigger = ["help"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        dispatcher = self.context.get("dispatcher")
        if not dispatcher:
            return "[Lex] Dispatcher not available."

        triggers = []
        for cmd in dispatcher.commands:
            trig = getattr(cmd, "trigger", [])
            if isinstance(trig, (list, tuple)):
                triggers.extend(trig)
        if not triggers:
            return "[Lex] No commands loaded."
        unique = sorted(set(triggers))
        return "[Lex] Available commands: " + ", ".join(unique)

