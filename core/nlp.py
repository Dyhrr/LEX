"""Natural language to command string conversion utilities."""

from dataclasses import dataclass
from typing import Callable, Iterable, List, Tuple

import json
import math
import os
import re
from difflib import get_close_matches

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib


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

# File storing user learned phrases
CUSTOM_INTENTS_FILE = os.path.join("memory", "custom_intents.json")

# Registry for user-defined intents
CUSTOM_REGISTRY = IntentRegistry()

_custom_cache: dict[str, str] | None = None

# ML model and training data paths
MODEL_FILE = os.path.join("models", "intent_classifier.pkl")
META_FILE = os.path.join("models", "intent_classifier_meta.json")
TRAINING_DATA_FILE = os.path.join("data", "training_data.json")

# Baseline examples to seed the classifier. These mirror the regex intents.
DEFAULT_TRAINING_DATA = [
    {"text": "remind me to buy milk", "command": "remind buy milk"},
    {"text": "set a reminder for cleaning", "command": "remind cleaning"},
    {"text": "what's the weather in paris", "command": "weather paris"},
    {"text": "flip a coin", "command": "game flip"},
    {"text": "roll a die", "command": "game roll"},
    {"text": "generate a uuid", "command": "tools uuid"},
    {"text": "generate a password 16", "command": "tools password 16"},
    {"text": "are you there", "command": "ping"},
]

MODEL = None


def _load_custom_intents() -> dict[str, str]:
    global _custom_cache
    if _custom_cache is not None:
        return _custom_cache
    if not os.path.exists(CUSTOM_INTENTS_FILE):
        _custom_cache = {}
        return _custom_cache
    try:
        with open(CUSTOM_INTENTS_FILE, "r", encoding="utf-8") as fh:
            _custom_cache = json.load(fh)
    except Exception:
        _custom_cache = {}
    return _custom_cache


def _save_custom_intents(data: dict[str, str]) -> None:
    os.makedirs(os.path.dirname(CUSTOM_INTENTS_FILE), exist_ok=True)
    with open(CUSTOM_INTENTS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def _refresh_custom_registry() -> None:
    CUSTOM_REGISTRY._intents.clear()
    for phrase, command in _load_custom_intents().items():
        pattern = re.compile(rf"^{re.escape(phrase)}$", re.I)
        CUSTOM_REGISTRY.register(pattern, lambda _m, c=command: c)


def add_custom_intent(phrase: str, command: str) -> None:
    data = _load_custom_intents()
    phrase = preprocess(phrase)
    data[phrase] = command
    _save_custom_intents(data)
    _refresh_custom_registry()


def get_custom_intents() -> dict[str, str]:
    return _load_custom_intents().copy()


def _load_training_data() -> list[dict[str, str]]:
    """Load user provided corrections from disk."""
    if not os.path.exists(TRAINING_DATA_FILE):
        return []
    try:
        with open(TRAINING_DATA_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def _save_training_data(data: list[dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(TRAINING_DATA_FILE), exist_ok=True)
    with open(TRAINING_DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def record_correction(original: str, corrected: str) -> None:
    """Persist a user correction for future training."""
    data = _load_training_data()
    data.append({"text": preprocess(original), "command": preprocess(corrected)})
    _save_training_data(data)


# Populate registry on import
_refresh_custom_registry()


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
    reg(r"^what features are you missing", lambda m: "features")
    reg(r"^what features do you lack", lambda m: "features")
    reg(r"^missing features", lambda m: "features")


register_default_intents()

_model_data_size: int = 0


def _train_model() -> None:
    """Train classifier from default and user-provided data."""
    global MODEL, _model_data_size
    dataset = DEFAULT_TRAINING_DATA + _load_training_data()
    if not dataset:
        MODEL = None
        return
    texts = [preprocess(d["text"]) for d in dataset]
    commands = [d["command"] for d in dataset]
    pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
    pipe.fit(texts, commands)
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(pipe, MODEL_FILE)
    with open(META_FILE, "w", encoding="utf-8") as fh:
        json.dump({"size": len(dataset)}, fh)
    MODEL = pipe
    _model_data_size = len(dataset)


def load_model() -> None:
    """Load the saved model or train a new one if needed."""
    global MODEL, _model_data_size
    dataset_size = len(DEFAULT_TRAINING_DATA) + len(_load_training_data())
    if os.path.exists(MODEL_FILE) and os.path.exists(META_FILE):
        try:
            with open(META_FILE, "r", encoding="utf-8") as fh:
                meta = json.load(fh)
            if meta.get("size") == dataset_size:
                MODEL = joblib.load(MODEL_FILE)
                _model_data_size = dataset_size
                return
        except Exception:
            pass
    _train_model()


def classify_intent(text: str) -> Tuple[str, float]:
    """Return classifier prediction and confidence."""
    if MODEL is None:
        load_model()
    if MODEL is None:
        return "unknown", 0.0
    cleaned = preprocess(text)
    proba = MODEL.predict_proba([cleaned])[0]
    idx = int(proba.argmax())
    return MODEL.classes_[idx], float(proba[idx])


def regex_fallback(text: str) -> str:
    """Fallback to regex-based intent matching."""
    result = CUSTOM_REGISTRY.parse(text)
    if result != text:
        return result
    return REGISTRY.parse(text)


def fuzzy_match(text: str, choices: Iterable[str], cutoff: float = 0.75) -> str | None:
    """Return text with the closest trigger substituted when similar."""
    matches = get_close_matches(text, choices, n=1, cutoff=cutoff)
    if matches:
        return matches[0]
    parts = text.split(maxsplit=1)
    if not parts:
        return None
    first = parts[0]
    rest = parts[1] if len(parts) > 1 else ""
    matches = get_close_matches(first, choices, n=1, cutoff=cutoff)
    if matches:
        return f"{matches[0]} {rest}".strip()
    return None


def update_model_on_corrections() -> None:
    """Retrain model if new corrections were recorded."""
    dataset_size = len(DEFAULT_TRAINING_DATA) + len(_load_training_data())
    if dataset_size != _model_data_size:
        _train_model()


def normalize_input(
    text: str, choices: Iterable[str] | None = None, cutoff: float = 0.75
) -> str:
    """Normalize user text into a command using ML, regex and fuzzy matching."""

    cleaned = preprocess(text)
    intent, conf = classify_intent(cleaned)
    if intent != "unknown" and conf >= 0.6:
        return intent
    result = regex_fallback(cleaned)
    if result != cleaned:
        return result
    if choices:
        match = fuzzy_match(cleaned, choices, cutoff=cutoff)
        if match:
            return match
    return cleaned


if __name__ == "__main__":
    # Minimal inline tests for manual execution. These do not replace pytest.
    load_model()
    assert normalize_input("Remind me to drink") == "remind drink"
    assert normalize_input("  how's the weather in Tokyo?  ") == "weather Tokyo"
    assert normalize_input("Flip a coin!") == "game flip"
    assert normalize_input("Generate a password of length 16") == "tools password 16"

    original = "Whats weather"
    corrected = "weather Berlin"
    record_correction(original, corrected)
    update_model_on_corrections()
    assert normalize_input(original) == corrected
    print("All inline NLP tests passed.")
