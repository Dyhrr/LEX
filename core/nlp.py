"""Natural language to command string conversion utilities."""

from dataclasses import dataclass
from typing import Callable, List

import re


@dataclass
class Intent:
    """Represents a single intent pattern and its handler."""

    pattern: re.Pattern[str]
    handler: Callable[[re.Match[str]], str]


class IntentRegistry:
    """Registry maintaining all available NLP intents."""

    def __init__(self) -> None:
        self._intents: List[Intent] = []

    def register(
        self, pattern: str | re.Pattern[str], handler: Callable[[re.Match[str]], str], flags: int = re.I
    ) -> None:
        """Register a new intent with its associated pattern and handler."""

        if isinstance(pattern, str):
            pattern = re.compile(pattern, flags)
        self._intents.append(Intent(pattern, handler))

    def parse(self, text: str) -> str:
        """Parse the given text and return the canonical command string."""

        cleaned = preprocess(text)
        for intent in self._intents:
            match = intent.pattern.match(cleaned)
            if match:
                return intent.handler(match).strip()
        # No pattern matched; return cleaned text as-is
        return cleaned


def preprocess(text: str) -> str:
    """Normalize whitespace, capitalization and punctuation."""

    cleaned = text.strip()
    # collapse multiple spaces and remove trailing punctuation
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" .,!?")
    return cleaned


# Global registry of default intents. Registration order matters.
REGISTRY = IntentRegistry()


def register_default_intents() -> None:
    """Populate the intent registry with built-in patterns."""

    reg = REGISTRY.register

    # Reminders
    reg(r"^(?:please\s+)?remind me to (.+)", lambda m: f"remind {m.group(1)}")
    reg(r"^(?:can|could) you remind me to (.+)", lambda m: f"remind {m.group(1)}")
    reg(r"^set a reminder for (.+)", lambda m: f"remind {m.group(1)}")
    reg(r"^(?:can|could) you set a reminder for (.+)", lambda m: f"remind {m.group(1)}")
    reg(r"^tell me to (.+)", lambda m: f"remind {m.group(1)}")

    # Weather
    reg(r"^what(?:'s| is) the weather(?: in| for)?\s*(.*)", lambda m: f"weather {m.group(1).strip()}")
    reg(r"^how(?:'s| is) the weather(?: in| for)?\s*(.*)", lambda m: f"weather {m.group(1).strip()}")
    reg(r"^what(?:'s| is) the weather like(?: in| for)?\s*(.*)", lambda m: f"weather {m.group(1).strip()}")

    # Simple games
    reg(r"^flip a coin", lambda m: "game flip")
    reg(r"^toss a coin", lambda m: "game flip")
    reg(r"^(?:can|could) you flip a coin", lambda m: "game flip")
    reg(r"^roll (?:a )?dice", lambda m: "game roll")
    reg(r"^throw (?:a )?dice", lambda m: "game roll")
    reg(r"^roll a die", lambda m: "game roll")
    reg(r"^(?:can|could) you roll (?:a )?dice", lambda m: "game roll")

    # Tools
    reg(r"^generate a uuid", lambda m: "tools uuid")
    reg(r"^(?:give|make) me a uuid", lambda m: "tools uuid")
    reg(r"^i need a uuid", lambda m: "tools uuid")
    reg(r"^generate a password(?: of length)? (\d+)", lambda m: f"tools password {m.group(1)}")
    reg(r"^i need a password(?: of length)? (\d+)", lambda m: f"tools password {m.group(1)}")
    reg(r"^generate a password", lambda m: "tools password")
    reg(r"^i need a password", lambda m: "tools password")

    # Ping / system info
    reg(r"^are you there", lambda m: "ping")
    reg(r"^are you awake", lambda m: "ping")


register_default_intents()


def normalize_input(text: str) -> str:
    """Public API used by the dispatcher."""

    return REGISTRY.parse(text)


if __name__ == "__main__":
    # Minimal inline tests for manual execution. These do not replace pytest.
    assert normalize_input("Remind me to drink") == "remind drink"
    assert normalize_input("  how's the weather in Tokyo?  ") == "weather Tokyo"
    assert normalize_input("Flip a coin!") == "game flip"
    print("All inline NLP tests passed.")
