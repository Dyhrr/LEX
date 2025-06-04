import asyncio
import json
import os

VAULT_FILE = os.path.join("memory", "vault.json")


class Command:
    trigger = ["vault"]

    def __init__(self, context):
        self.context = context

    async def _load(self) -> dict:
        if not os.path.exists(VAULT_FILE):
            return {}
        try:
            async with asyncio.Lock():
                with open(VAULT_FILE, "r", encoding="utf-8") as fh:
                    return json.load(fh)
        except Exception:
            return {}

    async def _save(self, data: dict) -> None:
        os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
        async with asyncio.Lock():
            with open(VAULT_FILE, "w", encoding="utf-8") as fh:
                json.dump(data, fh)

    async def run(self, args: str) -> str:
        """Simple vault to store and retrieve key/value pairs."""
        tokens = args.split(maxsplit=2)
        if not tokens:
            return "[Lex] Try 'vault list', 'vault get <key>' or 'vault set <key> <value>'."

        action = tokens[0]
        store = await self._load()

        if action == "list":
            return ", ".join(store.keys()) or "[Lex] Vault is empty."

        if action == "get" and len(tokens) > 1:
            return store.get(tokens[1], "[Lex] Not found.")

        if action == "set" and len(tokens) > 2:
            store[tokens[1]] = tokens[2]
            await self._save(store)
            return "[Lex] Stored."

        return "[Lex] Invalid vault command."
