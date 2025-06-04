import json
import os
import random
from functools import lru_cache

RESPONSES_FILE = os.path.join("personality", "responses.json")


@lru_cache(maxsize=1)
def load_responses() -> dict:
    """Load canned responses from disk with simple caching."""
    if not os.path.exists(RESPONSES_FILE):
        return {}
    try:
        with open(RESPONSES_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def get_sarcasm(settings: dict) -> str:
    """Return a sarcastic line based on the configured level."""
    level = int(settings.get("sarcasm_level", 5))
    responses = load_responses()
    key = f"sarcasm_{level}"
    lines = responses.get(key)
    if not lines:
        lines = responses.get("default", [])
    if not lines:
        return ""
    return random.choice(lines)


def get_response(category: str, settings: dict) -> str:
    """Return a category specific response or fallback to sarcasm."""
    responses = load_responses()
    options = responses.get(category, [])
    if not options:
        return get_sarcasm(settings)
    return random.choice(options)
