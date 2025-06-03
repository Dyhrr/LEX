import json
import os

DEFAULTS = {
    "sarcasm_level": 5,
    "use_cloud": False
}

def load_settings():
    if not os.path.exists("settings.json"):
        with open("settings.json", "w") as f:
            json.dump(DEFAULTS, f, indent=4)
        return DEFAULTS
    
    with open("settings.json") as f:
        settings = json.load(f)
    
    # Fill missing with defaults
    for key, value in DEFAULTS.items():
        settings.setdefault(key, value)
    return settings