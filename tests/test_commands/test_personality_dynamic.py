import json
import pytest
from personality import responder


def test_dynamic_loading(tmp_path, monkeypatch):
    file = tmp_path / "extra.json"
    file.write_text(json.dumps({"ping": ["dynamic"]}))
    monkeypatch.setattr(responder, "RESPONSES_DIR", tmp_path)
    responder.reload_responses()
    data = responder.load_responses()
    assert "dynamic" in data.get("ping", [])
