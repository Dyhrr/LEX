class Command:
    trigger = ["ping", "are you alive"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "[Lex] Pong. Unfortunately, yes, I'm still here."
