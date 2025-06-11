"""Adjust voice name, rate and pitch."""

import asyncio


class Command:
    description = "Adjust voice name, rate and pitch."
    """Adjust voice output settings like rate and pitch."""

    trigger = ["tone"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        settings = self.context.get("settings", {})
        tokens = args.split()

        if not tokens:
            name = settings.get("voice_name") or "default"
            rate = settings.get("voice_rate", 150)
            pitch = settings.get("voice_pitch", 50)
            return f"[Lex] Voice: {name} | Rate: {rate} | Pitch: {pitch}"

        action = tokens[0]

        if action == "rate" and len(tokens) > 1:
            try:
                rate = int(tokens[1])
            except ValueError:
                return "[Lex] Rate must be a number."
            settings["voice_rate"] = max(50, min(300, rate))
            return f"[Lex] Voice rate set to {settings['voice_rate']}"

        if action == "pitch" and len(tokens) > 1:
            try:
                pitch = int(tokens[1])
            except ValueError:
                return "[Lex] Pitch must be a number."
            settings["voice_pitch"] = max(0, min(100, pitch))
            return f"[Lex] Voice pitch set to {settings['voice_pitch']}"

        if action == "voice" and len(tokens) > 1:
            name = " ".join(tokens[1:])
            settings["voice_name"] = name
            return f"[Lex] Voice name set to {name}"

        if action == "reset":
            settings.update({"voice_name": "", "voice_rate": 150, "voice_pitch": 50})
            return "[Lex] Voice settings reset."

        return (
            "[Lex] Usage: tone rate <num> | pitch <num> | voice <name> | reset"
        )
