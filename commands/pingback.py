"""Check if a host is reachable via `ping`."""

import asyncio
import platform


class Command:
    description = "Check if a host is reachable via `ping`."
    """Check network reachability for a host."""

    trigger = ["pingback"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        host = args.strip() or "8.8.8.8"
        flag = "-n" if platform.system() == "Windows" else "-c"
        proc = await asyncio.create_subprocess_exec(
            "ping",
            flag,
            "1",
            host,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode == 0:
            return f"[Lex] {host} is reachable."
        return f"[Lex] {host} unreachable."
