import glob
import json
import os
import random

RESPONSES_DIR = os.path.join("personality")
_CACHE: dict | None = None
_MTIME: float = 0.0


def _current_mtime() -> float:
    times = []
    for path in glob.glob(os.path.join(RESPONSES_DIR, "*.json")):
        try:
            times.append(os.path.getmtime(path))
        except OSError:
            continue
    return max(times) if times else 0.0


def load_responses(force_reload: bool = False) -> dict:
    """Load and merge all personality JSON files."""
    global _CACHE, _MTIME
    mtime = _current_mtime()
    if force_reload or _CACHE is None or mtime != _MTIME:
        data: dict = {}
        for path in glob.glob(os.path.join(RESPONSES_DIR, "*.json")):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    part = json.load(fh)
                if isinstance(part, dict):
                    data.update(part)
            except Exception:
                continue
        _CACHE = data
        _MTIME = mtime
    return _CACHE or {}


def reload_responses() -> None:
    """Force reload personality data from disk."""
    load_responses(force_reload=True)


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
