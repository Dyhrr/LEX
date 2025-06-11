# TODO Modules

🔥 Critical (Breaks or Blocks UX)
 Add exception handling to all Command.run() calls

Prevent full crash when one plugin explodes

 Implement plugin sandboxing

Limit damage scope of a single broken plugin (timeouts? fallbacks?)

 Harden dangerous commands (e.g. kill)

Add user confirmation step or require explicit opt-in in settings.json

 Improve context structure

Avoid junk-drawer context usage — use sub-dicts (system, user, plugin)

🧠 Architecture Improvements
 Convert fuzzy matching logic into user-configurable threshold

Set threshold or disable fuzzy matching via settings.json

 Refactor dispatcher to include Command.help() support

Add built-in help, list, describe <command>

 Use watchdog for live plugin reload instead of polling

Cleaner, event-driven reload logic for hot-swapping

 Split voice/console modes into flags

Allow fixed mode selection instead of weird fallbacks

🧪 Testing & Stability
 Add unit tests for dispatcher routing

 Write test scaffolds for all plugins

 Mock voice input + TTS output for CI runs

 Add lex doctor to diagnose missing deps or invalid config

🔊 UX & Quality-of-Life
 Command auto-suggest on unknown trigger

“Did you mean: 'remind'?”

 Add --verbose and --quiet CLI flags

Toggle logging level without editing config

 Command usage logging + analytics (local only)

View what you use most and remove junk

 Dynamic personality loading (/personality/*.json)

Switch tone/response style mid-run

🌍 Optional/Long-Term
 Community plugin system (opt-in)

 Mobile bridge (via adb or local server)

 Support for GPT calls via local Ollama or cloud fallback

 Routine learning (simple habit memory)

🧾 Housekeeping
 Add plugin metadata linter (Command.trigger, Command.description)

 Add .env.example and better key loading (avoid hardcoding ElevenLabs keys in settings.json)

 Document every plugin with docstrings + markdown
