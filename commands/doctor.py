import asyncio
import importlib.util
import os
import sys

REQUIRED_PACKAGES = ["requests", "pyttsx3", "psutil"]


class Command:
    """Run basic diagnostic checks for the Lex environment."""

    trigger = ["doctor"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)

        issues = []

        if sys.version_info < (3, 11):
            issues.append("Python 3.11+ required")

        for pkg in REQUIRED_PACKAGES:
            if importlib.util.find_spec(pkg) is None:
                issues.append(f"Missing package: {pkg}")

        settings = self.context.get("settings", {})
        if (
            settings.get("use_cloud")
            and settings.get("tts_engine") == "elevenlabs"
        ):
            if not settings.get("elevenlabs_api_key") or not settings.get(
                "elevenlabs_voice_id"
            ):
                issues.append("ElevenLabs credentials not configured")

        data_dir = os.path.join(os.getcwd(), "memory")
        if not os.path.isdir(data_dir):
            issues.append("memory/ directory missing")

        if issues:
            joined = "\n".join(f"- {i}" for i in issues)
            return "[Lex] Doctor found issues:\n" + joined

        return "[Lex] System looks good."

