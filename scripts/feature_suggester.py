"""Suggest new NLP command patterns based on unhandled user inputs."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# Utility functions for handling data directory and log files
# ---------------------------------------------------------------------------

def ensure_data_dir() -> Path:
    """Ensure that the repo-level `data/` directory exists."""

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir


def load_unhandled() -> list[str]:
    """Load raw text strings from `unhandled_inputs.log`."""

    log_file = Path("data") / "unhandled_inputs.log"
    if not log_file.exists():
        return []

    texts: list[str] = []
    with log_file.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                text = record.get("text", "")
                if text:
                    texts.append(str(text))
            except json.JSONDecodeError:
                continue
    return texts


# ---------------------------------------------------------------------------
# Phrase normalization utilities
# ---------------------------------------------------------------------------

def normalize_phrase(phrase: str) -> str:
    """Lowercase and strip punctuation while preserving digits."""

    cleaned = phrase.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


# ---------------------------------------------------------------------------
# Pattern creation helpers
# ---------------------------------------------------------------------------

def propose_pattern_and_template(common_phrase: str) -> dict:
    """Create a regex pattern and template command from a phrase."""

    if re.search(r"\b\d+\b", common_phrase):
        pattern = re.sub(r"\b\d+\b", r"(\\d+)", common_phrase, count=1)
        pattern = f"^{pattern}$"
        return {
            "pattern": pattern,
            "template": "timer {group(1)}",
            "reason": "Detected numeric argument",
        }

    # No numeric tokens detected; produce a simple literal pattern
    pattern = f"^{common_phrase}$"
    return {
        "pattern": pattern,
        "template": common_phrase,
        "reason": "No numeric token detected",
    }


# ---------------------------------------------------------------------------
# Core suggestion generation
# ---------------------------------------------------------------------------

def cluster_and_create_suggestions(texts: list[str], min_occurrences: int = 3) -> dict:
    """Return suggested patterns for phrases meeting the occurrence threshold."""

    counter: Counter[str] = Counter(normalize_phrase(t) for t in texts if t)
    suggestions: dict[str, dict] = {}
    for phrase, count in counter.items():
        if count >= min_occurrences and phrase:
            suggestions[phrase] = propose_pattern_and_template(phrase)
    return suggestions


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_existing_suggestions() -> dict:
    """Load existing suggestions from the JSON file if present."""

    file = Path("data") / "feature_suggestions.json"
    if not file.exists():
        return {}
    try:
        with file.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def save_suggestions(all_suggestions: dict) -> None:
    """Write suggestions to `feature_suggestions.json`."""

    file = Path("data") / "feature_suggestions.json"
    with file.open("w", encoding="utf-8") as fh:
        json.dump(all_suggestions, fh, indent=2)


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point to read logs, generate suggestions and persist them."""

    ensure_data_dir()
    texts = load_unhandled()
    print(f"Loaded {len(texts)} unhandled inputs.")

    new_suggestions = cluster_and_create_suggestions(texts)
    print(f"Found {len(new_suggestions)} phrases meeting threshold.")

    existing = load_existing_suggestions()
    added = 0
    for phrase, info in new_suggestions.items():
        if phrase not in existing:
            existing[phrase] = info
            added += 1

    save_suggestions(existing)
    print(f"{added} new suggestion(s) written to data/feature_suggestions.json.")


if __name__ == "__main__":
    main()
