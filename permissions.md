# Plugin Permissions Model

Plugins can access:
- Files inside `/memory/` and `/core/`
- Whitelisted external processes only

Plugins cannot:
- Modify system files outside this project
- Launch network connections unless explicitly whitelisted in `settings.json`
