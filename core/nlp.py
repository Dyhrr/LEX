import re

# Simple patterns to convert natural phrases into Lex commands
PATTERNS: list[tuple[re.Pattern[str], callable]] = [
    # Reminders
    (re.compile(r"^(?:please\s+)?remind me to (.+)", re.I),
        lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^(?:can|could) you remind me to (.+)", re.I),
        lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^set a reminder for (.+)", re.I),
        lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^(?:can|could) you set a reminder for (.+)", re.I),
        lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^tell me to (.+)", re.I),
        lambda m: f"remind {m.group(1)}"),

    # Weather
    (re.compile(r"^what(?:'s| is) the weather(?: in| for)?\s*(.*)", re.I),
        lambda m: f"weather {m.group(1).strip()}"),
    (re.compile(r"^how(?:'s| is) the weather(?: in| for)?\s*(.*)", re.I),
        lambda m: f"weather {m.group(1).strip()}"),
    (re.compile(r"^what(?:'s| is) the weather like(?: in| for)?\s*(.*)", re.I),
        lambda m: f"weather {m.group(1).strip()}"),

    # Simple games
    (re.compile(r"^flip a coin", re.I), lambda m: "game flip"),
    (re.compile(r"^toss a coin", re.I), lambda m: "game flip"),
    (re.compile(r"^(?:can|could) you flip a coin", re.I), lambda m: "game flip"),
    (re.compile(r"^roll (?:a )?dice", re.I), lambda m: "game roll"),
    (re.compile(r"^throw (?:a )?dice", re.I), lambda m: "game roll"),
    (re.compile(r"^roll a die", re.I), lambda m: "game roll"),
    (re.compile(r"^(?:can|could) you roll (?:a )?dice", re.I), lambda m: "game roll"),

    # Tools
    (re.compile(r"^generate a uuid", re.I), lambda m: "tools uuid"),
    (re.compile(r"^(?:give|make) me a uuid", re.I), lambda m: "tools uuid"),
    (re.compile(r"^i need a uuid", re.I), lambda m: "tools uuid"),
    (re.compile(r"^generate a password(?: of length)? (\d+)", re.I),
        lambda m: f"tools password {m.group(1)}"),
    (re.compile(r"^i need a password(?: of length)? (\d+)", re.I),
        lambda m: f"tools password {m.group(1)}"),
    (re.compile(r"^generate a password", re.I), lambda m: "tools password"),
    (re.compile(r"^i need a password", re.I), lambda m: "tools password"),

    # Ping / system info
    (re.compile(r"^are you there", re.I), lambda m: "ping"),
    (re.compile(r"^are you awake", re.I), lambda m: "ping"),
]


def normalize_input(text: str) -> str:
    """Return a canonical command string from natural language."""
    cleaned = text.strip()
    for pattern, func in PATTERNS:
        match = pattern.match(cleaned)
        if match:
            return func(match).strip()
    return cleaned
