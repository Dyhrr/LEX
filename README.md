# 🧠 Lex – Your Personal, Local-First, Sarcastic AI Assistant

Lex is a small desktop assistant that lives entirely on your PC. It won't phone
home unless you explicitly allow it. Think **Jarvis** with more attitude and a
hard rule against cloud dependency.

---

## ⚙️ What It Is

Lex is a **modular, locally running assistant** designed to:
- Stay offline unless *you* say otherwise
- Be extended through simple plugin commands
- Talk back with sarcastic, human-like sass
- Automate boring tasks so you don’t forget to drink water (again)

## Installation
1. Clone the repo
2. `pip install -r requirements.txt`
3. `python lexd.py`

### ElevenLabs TTS (optional)
To use the ElevenLabs cloud voices you need to enable cloud mode and add your
API key and voice ID to `settings.json`:

```json
"use_cloud": true,
"tts_engine": "elevenlabs",
"elevenlabs_api_key": "YOUR_KEY",
"elevenlabs_voice_id": "VOICE_ID"
```

Lex will then stream audio from ElevenLabs and play it locally.

---

## ✅ What Actually Works Right Now

### Functional Core
- ✅ Modular plugin loader via `dispatcher.py`
- ✅ Async command processing (non-blocking CLI loop)
- ✅ Config loader with default injection (`settings.json`)
- ✅ Passphrase-protected startup with encrypted vault
- ✅ Fully offline (unless using `define`, which pings an API)
- ✅ Expanded natural language parsing for common phrases
- ✅ Fuzzy matching for misspelled commands
- ✅ Optional voice input and text-to-speech output

### Example Commands
- ✅ `remind me in X minutes to Y` (persistent reminders)
- ✅ `open notepad`, `search for cats`
- ✅ `kill discord` (taskkill whitelist-safe)
- ✅ `generate password`, `generate uuid`
- ✅ `flip a coin`, `roast me`, `compliment me`
- ✅ `define <word>` (real API based)
- ✅ `weather` (mocked for now)
- ✅ `vault` with passphrase-encrypted storage
- ✅ Natural phrasing like "can you remind me to drink" or "how's the weather"
- ✅ Teach Lex new phrases with `learn <phrase> as <command>`
- ✅ `search index` then `search <file>` to locate files
- ✅ `clipboard add <text>` and `clipboard paste`
- ✅ `notes add <text>` for a quick local wiki
- ✅ `health` to check CPU, RAM and disk usage

---

## 🛣 Roadmap

### 🚧 Short-Term
- [x] Voice input via Whisper or `speech_recognition`
- [x] Text-to-speech output (pyttsx3, ElevenLabs optional)
- [ ] Plugin hot reloading
- [ ] Debug dashboard or CLI monitor
- [ ] Cross-platform support (Linux/macOS compatibility)

### 🧠 Future Ideas
- [ ] Routine learning
- [ ] Context tracking for multi-step conversations
- [ ] Plugin marketplace or repo sync
- [ ] Sarcasm tone slider in `settings.json` (because chaos)

---

## 📂 Folder Structure
LEX/
├── lexd.py           # Main async loop
├── dispatcher.py     # Plugin command router
├── settings.json     # Global config
├── core/             # Core settings/utils
├── commands/         # Your plugin modules
├── memory/           # Persistent storage (reminders, vault)
├── personality/      # Tone files, sass library
---

See [AGENTS.md](AGENTS.md) for additional contributor notes and advanced usage tips.

## 🧩 Commands & Plugins

All plugins live in the `commands/` folder. Any module that exposes a `Command` class with a `trigger` list and an asynchronous `run()` method is picked up automatically by `dispatcher.py`.

```python
class Command:
    trigger = ["ping"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "Pong!"


All plugins live in the `commands/` folder. The dispatcher scans that directory
at startup and imports any module exposing a `Command` class. Each command lists
one or more trigger words in `trigger` and implements an asynchronous `run()`
method.

```python
class Command:
    trigger = ["ping"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "Pong!"
```

Responses are returned as plain text for now. Voice input and text-to-speech are
planned but optional—the command system works fine without them.

When writing a plugin, keep it async-friendly. Long-running work should be done
with asyncio-compatible libraries to avoid blocking the event loop. The context
dict passed to each `Command` can be used to access settings or share state.


💡 **Design Philosophy**
Lex is:

- Local-first—no cloud calls unless `use_cloud` is enabled
- Sarcastic by default
- Lightweight (no gigabyte RAM usage just to say "hi")

He’s meant to be:

- Expandable through simple plugins
- Helpful with a side of attitude
- Dumb enough to stay local, smart enough to feel personal

🔒 **License**
MIT License. No analytics, no telemetry—just you, your PC, and an assistant with attitude.

🐢 **Credits**
Created by Dyhrrr, the sort of developer who'd rather automate life than organize it.

"Built to automate my life, so I can keep ignoring it."
