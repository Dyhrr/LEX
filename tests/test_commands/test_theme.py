import json
import pytest

from commands import theme


@pytest.mark.asyncio
async def test_theme_updates_settings(tmp_path, monkeypatch):
    themes = tmp_path / "themes"
    themes.mkdir()
    (themes / "lex.css").write_text("")
    (themes / "meme.css").write_text("")
    settings_file = tmp_path / "settings.json"
    monkeypatch.setattr(theme, "THEMES_DIR", themes)
    monkeypatch.setattr(theme, "SETTINGS_FILE", settings_file)

    settings = {}
    cmd = theme.Command({"settings": settings})
    resp = await cmd.run("meme")
    assert "meme" in resp or settings.get("theme") == "meme"
    data = json.load(open(settings_file))
    assert data["theme"] == "meme"
