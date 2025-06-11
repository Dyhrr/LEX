"""Show basic system information."""

import asyncio
import platform
import os
import shutil


class Command:
    description = "Show basic system information."
    trigger = ["system"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        """Return basic system information."""
        await asyncio.sleep(0)

        uname = platform.uname()
        total, used, free = shutil.disk_usage(os.path.sep)
        try:
            load1, load5, load15 = os.getloadavg()
            load_info = f"Load avg: {load1:.2f}, {load5:.2f}, {load15:.2f}"
        except OSError:
            load_info = "Load avg: N/A"

        info = [
            f"System: {uname.system} {uname.release}",
            f"Machine: {uname.machine}",
            f"Disk: {used // (1024**3)}GB used / {total // (1024**3)}GB", 
            load_info,
        ]

        return "[Lex] " + " | ".join(info)
