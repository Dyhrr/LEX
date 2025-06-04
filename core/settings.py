import json
import os

DEFAULTS = {"sarcasm_level": 5, "use_cloud": False}


def load_settings(path: str = "settings.json") -> dict:
    """Load settings from a JSON file, falling back to defaults."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as e:
            print(f"[Lex] ERROR loading settings: {e}")
    return DEFAULTS.copy()
