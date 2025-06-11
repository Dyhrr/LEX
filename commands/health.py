"""Report basic CPU, RAM and disk usage."""

import asyncio

import psutil


class Command:
    description = "Report basic CPU, RAM and disk usage."
    """Report basic system health."""

    trigger = ["health", "stats"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        info = [
            f"CPU: {cpu}%",
            f"RAM: {mem.percent}%",
            f"Disk: {disk.percent}%",
        ]
        return "[Lex] " + " | ".join(info)
