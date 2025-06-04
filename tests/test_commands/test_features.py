import json
import pytest

from commands import features


@pytest.mark.asyncio
async def test_features_list(tmp_path, monkeypatch):
    file = tmp_path / "feature_suggestions.json"
    data = {"brew coffee": {"pattern": "^brew coffee$"}}
    file.write_text(json.dumps(data))
    monkeypatch.setattr(features, "SUGGESTIONS_FILE", file)
    cmd = features.Command({})
    result = await cmd.run("")
    assert "brew coffee" in result
