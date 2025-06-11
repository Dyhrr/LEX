class Command:
    trigger = ["weather"]

    def __init__(self, context):
        self.context = context
        self.settings = context.get("settings", {})

    async def run(self, args: str) -> str:
        """Return a weather report using a local or cloud source."""
        location = args.strip() or "your area"
        if not self.settings.get("use_cloud"):
            return f"[Lex] It's probably fine outside in {location}."
        import asyncio, requests
        url = f"https://wttr.in/{location}?format=3"
        try:
            resp = await asyncio.to_thread(requests.get, url, timeout=5)
            return resp.text.strip()
        except Exception as e:
            return f"[Lex] Couldn't fetch weather for {location}: {e}"
