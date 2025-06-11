# Lex TODO — Dev Tasks & Roadmap

---

## 🔥 Critical (Breaks UX or Causes Crashes)

- [ ] Add exception handling to all `Command.run()` calls  
      → Prevent whole-system crash when a plugin explodes

- [ ] Implement plugin sandboxing  
      → Timeout or fallback if a plugin stalls or fails

- [ ] Harden dangerous commands (e.g. `kill`)  
      → Add opt-in flags or explicit confirmations via settings

- [ ] Improve `context` structure  
      → Avoid dumping everything into one dict — separate into `system`, `user`, `plugin`

---

## 🧠 Architecture & Core Improvements

- [ ] Refactor `dispatcher` to support `Command.help()`  
      → Built-in `help`, `list`, `describe <command>` support

- [ ] Replace plugin polling with `watchdog` FS events  
      → Real-time hot reload for plugins

- [ ] Split CLI vs Voice mode with flags  
      → Remove auto-fallback behavior, allow deterministic launch mode

---

## 🧪 Testing & Stability

- [ ] Add unit tests for dispatcher routing
- [ ] Write basic test scaffolds for all plugins
- [ ] Mock voice input / TTS output for CI testing
- [x] Add `lex doctor` diagnostic command
      → Check for missing deps, bad config, incompatible Python, etc.

---

## 🔊 UX & Quality-of-Life

- [ ] Command auto-suggest on unknown triggers  
      → “Did you mean: remind?”

- [ ] Local command usage logging + frequency analytics  
      → View most-used plugins and drop unused ones

- [ ] Add dynamic personality loading  
      → Load `/personality/*.json` at runtime (switch tone mid-session)

---

## 🌍 Optional / Long-Term

- [ ] Community plugin loader (opt-in, sandboxed)
- [ ] Mobile bridge via ADB or local tunnel
- [ ] GPT integration via Ollama or cloud fallback
- [ ] Simple habit/routine memory for learning user behavior

---

## 🧾 Housekeeping / Dev Quality

- [x] Add `.env.example` + load secrets from env properly
      → Avoid leaking ElevenLabs keys in `settings.json`

- [ ] Document each plugin:
    - Docstrings for internal help
    - Markdown table for plugin overview
