import json
import os
from .logger import get_logger

DEFAULTS = {
    "sarcasm_level": 5,
    "use_cloud": False,
    "voice_input": True,
    "voice_output": True,
    "tts_engine": "pyttsx3",
    "voice_name": "",
    "voice_rate": 150,
    "voice_pitch": 50,
    "elevenlabs_api_key": "",
    "elevenlabs_voice_id": "",
}


logger = get_logger()


def load_settings(path: str = "settings.json") -> dict:
    """Load settings from a JSON file, falling back to defaults."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as e:
            logger.error("ERROR loading settings: %s", e)
    return DEFAULTS.copy()
