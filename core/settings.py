import json
import os
from .logger import get_logger
from dotenv import load_dotenv

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
    "plugin_timeout": 5.0,
    "allow_process_terminate": False,
    "theme": "lex",
}


logger = get_logger()


def load_settings(path: str = "settings.json") -> dict:
    """Load settings from a JSON file, merging with defaults."""
    # Load environment variables from a local .env file if present
    load_dotenv(override=False)

    data = DEFAULTS.copy()

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                file_data = json.load(fh)
            if isinstance(file_data, dict):
                data.update(file_data)
        except Exception as e:
            logger.error("ERROR loading settings: %s", e)

    # Override sensitive values from environment variables when available
    env_map = {
        "elevenlabs_api_key": os.getenv("ELEVENLABS_API_KEY"),
        "elevenlabs_voice_id": os.getenv("ELEVENLABS_VOICE_ID"),
    }
    for key, value in env_map.items():
        if value:
            data[key] = value

    return data


def save_settings(data: dict, path: str = "settings.json") -> None:
    """Write settings to disk."""
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    except Exception as e:
        logger.error("ERROR saving settings: %s", e)
