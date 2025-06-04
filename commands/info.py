import asyncio


class Command:
    trigger = ["info"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """List loaded commands and current settings."""
        await asyncio.sleep(0)

        settings = self.context.get("settings", {})
        cmds = self.context.get("commands", {})
        triggers = []
        for cmd in cmds.values():
            triggers.extend(getattr(cmd, "trigger", []))

        trigger_list = ", ".join(sorted(triggers)) or "none"
        sarcasm = settings.get("sarcasm_level", "?")

        return f"[Lex] Commands: {trigger_list} | Sarcasm level: {sarcasm}"
