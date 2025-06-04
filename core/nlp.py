import re

# Simple patterns to convert natural phrases into Lex commands
PATTERNS: list[tuple[re.Pattern[str], callable]] = [
    (re.compile(r"^remind me to (.+)", re.I), lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^set a reminder for (.+)", re.I), lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^tell me to (.+)", re.I), lambda m: f"remind {m.group(1)}"),
    (re.compile(r"^what(?:'s| is) the weather(?: in| for)?\s*(.*)", re.I), lambda m: f"weather {m.group(1).strip()}"),
    (re.compile(r"^flip a coin", re.I), lambda m: "game flip"),
    (re.compile(r"^roll (?:a )?dice", re.I), lambda m: "game roll"),
    (re.compile(r"^roll a die", re.I), lambda m: "game roll"),
    (re.compile(r"^generate a uuid", re.I), lambda m: "tools uuid"),
    (re.compile(r"^generate a password(?: of length)? (\d+)", re.I), lambda m: f"tools password {m.group(1)}"),
    (re.compile(r"^generate a password", re.I), lambda m: "tools password"),
]


def normalize_input(text: str) -> str:
    """Return a canonical command string from natural language."""
    cleaned = text.strip()
    for pattern, func in PATTERNS:
        match = pattern.match(cleaned)
        if match:
            return func(match).strip()
    return cleaned
