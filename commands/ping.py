"""Respond with a simple \"Pong\" message."""

class Command:
    description = 'Respond with a simple "Pong" message.'
    trigger = ["ping", "are you alive"]

    def __init__(self, context):
        self.context = context
        self.settings = context.get("settings", {})

    async def run(self, args: str) -> str:
        """Reply with a simple pong message."""
        from personality.responder import get_response

        reply = get_response("ping", self.settings)
        return f"[Lex] Pong. {reply}"
