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
    "fuzzy_threshold": 0.75,
}


logger = get_logger()


def load_settings(path: str = "settings.json") -> dict:
    """Load settings from a JSON file, merging with defaults."""
    data = DEFAULTS.copy()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                file_data = json.load(fh)
            if isinstance(file_data, dict):
                data.update(file_data)
        except Exception as e:
            logger.error("ERROR loading settings: %s", e)
    return data
