class Command:
    trigger = ["ping", "are you alive"]

    def __init__(self, context):
        self.context = context
        self.settings = context.get("settings", {})

    async def run(self, args: str) -> str:
        from personality.responder import get_response

        reply = get_response("ping", self.settings)
        return f"[Lex] Pong. {reply}"
