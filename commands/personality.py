import asyncio


class Command:
    trigger = ["personality"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """Get or set sarcasm level."""
        settings = self.context.get("settings", {})
        from personality import responder
        responder.reload_responses()
        arg = args.strip()
        await asyncio.sleep(0)

        if arg:
            try:
                level = int(arg)
            except ValueError:
                return "[Lex] Give me a number between 0 and 10."
            level = max(0, min(10, level))
            settings["sarcasm_level"] = level
            from personality.responder import get_response

            level_str = str(level)
            resp = get_response(f"sarcasm_{level_str}", settings)
            return f"[Lex] Sarcasm level set to {level}. {resp}"

        level = settings.get("sarcasm_level", "unknown")
        from personality.responder import get_response

        level_str = str(level)
        resp = get_response(f"sarcasm_{level_str}", settings)
        return f"[Lex] Current sarcasm level: {level}. {resp}"
