# 🧠 Lex – Your Personal, Local-First AI Assistant

Lex is a disciplined desktop assistant that operates entirely on your PC. Designed for precision, privacy, and control, Lex executes tasks, manages routines, and automates daily functions—all without relying on the cloud unless explicitly permitted.

Think **Jarvis**—focused, secure, and capable. A digital butler designed to support your work, your schedule, and your systems.

## ⚙️ What It Is

Lex is a **modular, locally running assistant** developed to:
- Remain fully offline unless cloud access is explicitly enabled
- Execute custom commands via lightweight plugin modules
- Automate routine or repetitive actions efficiently
- Assist in day-to-day workflows with voice or text input

## Installation
Lex targets **Python 3.11+**. Once you have the correct version installed:
1. Clone the repository
2. `pip install -r requirements.txt`
3. `python lexd.py`

### ElevenLabs TTS (optional)
Lex can speak using the local `pyttsx3` engine or stream audio from ElevenLabs.
To enable cloud-based text-to-speech, set `use_cloud` to `true` and configure your credentials in `settings.json`:

```json
"use_cloud": true,
"tts_engine": "elevenlabs",
"elevenlabs_api_key": "YOUR_KEY",
"elevenlabs_voice_id": "VOICE_ID"
```

Lex will then stream and play back voice responses from ElevenLabs.

Audio playback is handled via the `simpleaudio` package for maximum cross-platform support.

### Voice Input (optional)
Lex listens using `speech_recognition`. When the Whisper package is installed, it falls back to Whisper for better accuracy. If `use_cloud` is `false`, all recognition happens locally; otherwise you may configure a cloud recognizer in the future.

### Textual UI (optional)
Run the interactive TUI with:

```bash
python textual_ui.py
```

Add `--sidebar` to display available command triggers in a side panel.

## ✅ What Works Now

### Functional Core
- ✅ Modular plugin loader (`dispatcher.py`)
- ✅ Async command loop (non-blocking architecture)
- ✅ Config loader with defaults (`settings.json`)
- ✅ Encrypted passphrase-protected vault (Fernet-encrypted `memory/vault.json` with PBKDF2-derived key)
- ✅ Fully offline functionality (API access only when allowed)
- ✅ Fuzzy matching and natural phrase interpretation
- ✅ Optional voice input + TTS output

### Supported Commands
- ✅ `remind me in X minutes to Y` (with persistence)
- ✅ `open notepad`, `search for cats`
- ✅ `kill discord` (whitelisted safe process management)
- ✅ `generate password`, `generate uuid`
- ✅ `flip a coin`, `define <word>`
- ✅ `weather` (mocked placeholder)
- ✅ Secure vault for sensitive data
- ✅ Clipboard and notes system
- ✅ Local system health monitoring (`health`)

## 🛣 Roadmap

### 🚧 Short-Term
- [x] Whisper-based or SpeechRecognition voice input
- [x] TTS via pyttsx3 or ElevenLabs
- [ ] Plugin hot reloading
- [ ] Debug CLI or optional UI panel
- [ ] Cross-platform polish (Linux/macOS support)

### 🧠 Future Goals
- [ ] Routine pattern recognition
- [ ] Multi-step conversation tracking
- [ ] Plugin syncing or community library
- [ ] Dynamic personality profiles

## 📂 Folder Structure
LEX/
├── lexd.py           # Core event loop  
├── dispatcher.py     # Plugin command router  
├── settings.json     # Global configuration  
├── core/             # Utilities and shared logic  
├── commands/         # Modular plugin commands  
├── memory/           # Persistence layer  
├── personality/      # (Optional) tone or behavioral modifiers  

## 🧩 Plugin System

All plugins reside in the `commands/` folder. The dispatcher imports any module exposing a `Command` class with a `trigger` list and an async `run()` method.

```python
class Command:
    trigger = ["ping"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "Pong."
```

Each command receives a **context** dictionary. It exposes:
- `settings`: parsed `settings.json`
- `logger`: the shared logger from `core/logger.py`
- `dispatcher`: the dispatcher instance (for hot reloading or dispatching new commands)
- `history`: recent `(command, result)` tuples
Additional keys may be added by future plugins.

The dispatcher can optionally watch for file changes and reload plugins on the fly when `Dispatcher.watch_modules()` is running.

Plugins are expected to be well-behaved: only whitelisted process names may be terminated and file access should stay within the project directory unless explicitly allowed.

## 🧭 Design Principles

- **Local-first**: All logic and data remain offline by default
- **Opt-in cloud**: Network APIs only activate when `use_cloud` is true in `settings.json` (set it to `false` for an offline-only setup)
- **Lightweight**: Designed for idle efficiency with low resource usage
- **Modular**: Extendable via drop-in plugins  
- **Respectful**: Secure, quiet, and efficient—always serving, never spying

## 🧪 Testing
Run the test suite with `pytest tests/` to validate plugins and the dispatcher. New commands should include corresponding tests in `tests/`.

## 🔒 License
MIT. No telemetry, no data collection, no analytics. Just you and your system.

## 🧾 Author
Created by Dyhrrr—a developer dedicated to building tools that serve with discretion and reliability.
