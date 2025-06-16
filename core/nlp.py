"""
Lex NLP Module — Refactored for precision, speed, and modularity
"""

import os
import re
import json
from typing import Callable, Iterable, List, Tuple, Literal
from dataclasses import dataclass

from rapidfuzz import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

# === Data Classes === #
@dataclass
class Intent:
    pattern: re.Pattern[str]
    handler: Callable[[re.Match[str]], str]
    priority: Literal['custom', 'default']

@dataclass
class NLPResult:
    command: str
    origin: str
    confidence: float
    raw_input: str

# === Paths === #
CUSTOM_INTENTS_FILE = os.path.join("memory", "custom_intents.json")
TRAINING_DATA_FILE = os.path.join("data", "training_data.json")
MODEL_FILE = os.path.join("models", "intent_classifier.pkl")
META_FILE = os.path.join("models", "intent_classifier_meta.json")

# === Core NLP Engine === #
class IntentRegistry:
    def __init__(self):
        self._intents: List[Intent] = []

    def register(self, pattern: str, handler: Callable[[re.Match[str]], str], priority='default', flags=re.I):
        compiled = re.compile(pattern, flags)
        self._intents.append(Intent(compiled, handler, priority))

    def match(self, text: str) -> Tuple[str, str]:
        for intent in sorted(self._intents, key=lambda i: i.priority == 'custom', reverse=True):
            match = intent.pattern.match(text)
            if match:
                return intent.handler(match).strip(), intent.priority
        return text, 'none'

# === NLP Utils === #
def preprocess(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip(" .,!?\n")).lower()

# === NLP Model === #
class IntentClassifier:
    def __init__(self):
        self.model = None
        self.size = 0

    def train(self, dataset: List[dict[str, str]]):
        texts = [preprocess(d['text']) for d in dataset]
        commands = [d['command'] for d in dataset]
        self.model = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
        self.model.fit(texts, commands)
        joblib.dump(self.model, MODEL_FILE)
        with open(META_FILE, "w") as fh:
            json.dump({"size": len(dataset)}, fh)
        self.size = len(dataset)

    def load_or_train(self):
        dataset = DEFAULT_TRAINING_DATA + _load_json_file(TRAINING_DATA_FILE)
        if os.path.exists(MODEL_FILE) and os.path.exists(META_FILE):
            try:
                with open(META_FILE) as fh:
                    meta = json.load(fh)
                if meta.get("size") == len(dataset):
                    self.model = joblib.load(MODEL_FILE)
                    self.size = meta["size"]
                    return
            except Exception:
                pass
        self.train(dataset)

    def classify(self, text: str) -> Tuple[str, float]:
        if not self.model:
            return "unknown", 0.0
        probs = self.model.predict_proba([text])[0]
        idx = int(probs.argmax())
        return self.model.classes_[idx], float(probs[idx])

# === NLP Main === #
REGISTRY = IntentRegistry()
CLASSIFIER = IntentClassifier()

# === NLP Interface === #
def normalize_input(text: str, plugin_choices: Iterable[str] | None = None, cutoff: float = 0.75) -> NLPResult:
    raw = text
    text = preprocess(text)

    intent, confidence = CLASSIFIER.classify(text)
    if confidence >= 0.6 and intent != "unknown":
        return NLPResult(intent, 'ml', confidence, raw)

    fallback, origin = REGISTRY.match(text)
    if origin != 'none':
        return NLPResult(fallback, origin, 1.0, raw)

    if plugin_choices:
        match = fuzzy_match(text, plugin_choices, cutoff)
        if match:
            return NLPResult(match, 'fuzzy', 0.7, raw)

    return NLPResult(text, 'raw', 0.0, raw)

# === Helpers === #
def fuzzy_match(text: str, choices: Iterable[str], cutoff=0.75) -> str | None:
    result = process.extractOne(text, choices, score_cutoff=cutoff * 100)
    return result[0] if result else None

def _load_json_file(path: str) -> List[dict]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []

# === Custom Intent System === #
def add_custom_intent(phrase: str, command: str):
    phrase = preprocess(phrase)
    intents = _load_json_file(CUSTOM_INTENTS_FILE)
    intents[phrase] = command
    os.makedirs(os.path.dirname(CUSTOM_INTENTS_FILE), exist_ok=True)
    with open(CUSTOM_INTENTS_FILE, "w") as fh:
        json.dump(intents, fh)
    REGISTRY.register(rf"^{re.escape(phrase)}$", lambda _: command, priority='custom')

# === Default Data === #
DEFAULT_TRAINING_DATA = [
    {"text": "remind me to drink water", "command": "remind drink water"},
    {"text": "flip a coin", "command": "game flip"},
    {"text": "generate a uuid", "command": "tools uuid"},
    {"text": "roll a die", "command": "game roll"},
    {"text": "weather in tokyo", "command": "weather tokyo"},
]

# === Register defaults === #
def register_default_intents():
    reg = REGISTRY.register
    reg(r"^remind me to (.+)", lambda m: f"remind {m.group(1)}")
    reg(r"^flip a coin", lambda _: "game flip")
    reg(r"^roll a die", lambda _: "game roll")
    reg(r"^generate a uuid", lambda _: "tools uuid")
    reg(r"^weather(?: in)? (.+)", lambda m: f"weather {m.group(1)}")

# === Bootstrap === #
register_default_intents()
CLASSIFIER.load_or_train()
