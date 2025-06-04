import asyncio
import secrets
import string
import uuid


class Command:
    trigger = ["tools"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """Generate simple utilities like UUIDs or passwords."""
        cmd = args.strip().lower()
        await asyncio.sleep(0)

        if cmd.startswith("uuid"):
            return str(uuid.uuid4())

        if cmd.startswith("password"):
            parts = cmd.split()
            length = 12
            if len(parts) > 1:
                try:
                    length = int(parts[1])
                except ValueError:
                    pass
            alphabet = string.ascii_letters + string.digits
            pwd = "".join(secrets.choice(alphabet) for _ in range(length))
            return pwd

        return "[Lex] Use 'tools uuid' or 'tools password <len>'."
