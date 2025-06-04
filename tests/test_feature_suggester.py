import pytest
from scripts.feature_suggester import (
    normalize_phrase,
    propose_pattern_and_template,
    cluster_and_create_suggestions,
)


def test_normalize_phrase_removes_punctuation_and_lowercases():
    assert normalize_phrase("Hello, WORLD!!") == "hello world"
    assert normalize_phrase("  multiple   spaces ") == "multiple spaces"
    assert normalize_phrase("Digits 123 and punctuation!") == "digits 123 and punctuation"


def test_propose_with_numeric_token():
    result = propose_pattern_and_template("set a 10 minute timer")
    assert result["pattern"] == r"^set a (\d+) minute timer$"
    assert result["template"] == "timer {group(1)}"
    assert "Detected numeric argument" in result["reason"]


def test_propose_without_numeric_token():
    result = propose_pattern_and_template("brew me coffee")
    assert result["pattern"] == r"^brew me coffee$"
    assert result["template"] == "brew me coffee"
    assert "No numeric token detected" in result["reason"]


def test_cluster_and_create_suggestions_basic():
    texts = ["foo", "foo", "bar"]
    suggestions = cluster_and_create_suggestions(texts, min_occurrences=2)
    assert "foo" in suggestions
    assert suggestions["foo"]["template"] in ["timer {group(1)}", "foo"]
