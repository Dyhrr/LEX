import asyncio
import json
import os
from cryptography.fernet import Fernet

VAULT_FILE = os.path.join("memory", "vault.json")


class Command:
    trigger = ["vault"]

    def __init__(self, context):
        self.context = context
        self.file = VAULT_FILE
        self.key: bytes | None = context.get("vault_key")
        self.lock = asyncio.Lock()

    def _read_json(self) -> dict:
        if not os.path.exists(self.file):
            return {}
        try:
            if self.key:
                with open(self.file, "rb") as fh:
                    data = fh.read()
                try:
                    decrypted = Fernet(self.key).decrypt(data)
                except Exception:
                    return {}
                return json.loads(decrypted.decode("utf-8"))
            with open(self.file, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}

    def _write_json(self, data: dict) -> None:
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        if self.key:
            token = Fernet(self.key).encrypt(json.dumps(data).encode())
            with open(self.file, "wb") as fh:
                fh.write(token)
        else:
            with open(self.file, "w", encoding="utf-8") as fh:
                json.dump(data, fh)

    async def _load(self) -> dict:
        async with self.lock:
            return await asyncio.to_thread(self._read_json)

    async def _save(self, data: dict) -> None:
        async with self.lock:
            await asyncio.to_thread(self._write_json, data)

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
