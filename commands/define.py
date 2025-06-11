"""Look up word definitions using a web API when cloud access is allowed."""

class Command:
    description = "Look up word definitions using a web API when cloud access is allowed."
    trigger = ["define"]

    def __init__(self, context):
        self.context = context
        self.settings = context.get("settings", {})

    async def run(self, args: str) -> str:
        """Look up a word using an online dictionary API when allowed."""
        word = args.strip()
        if not word:
            return "[Lex] Define what exactly?"
        if not self.settings.get("use_cloud"):
            return f"[Lex] Can't look up '{word}' without cloud access."
        import asyncio, requests
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            resp = await asyncio.to_thread(requests.get, url, timeout=5)
            data = resp.json()
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return f"{word}: {meaning}"
        except Exception as e:
            return f"[Lex] Couldn't fetch definition: {e}"
