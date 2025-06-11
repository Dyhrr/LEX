# Plugin Permissions Model

Plugins can access:
- Files inside `/memory/` and `/core/`
- Whitelisted external processes only

Plugins cannot:
- Modify system files outside this project
- Launch network connections unless explicitly whitelisted in `settings.json`

## Future Granularity

Additional permissions may restrict plugins to specific subfolders or
allow read-only access. When implemented, each plugin will declare the
exact paths and capabilities it requires. The dispatcher will enforce
those limits to keep plugins sandboxed.
