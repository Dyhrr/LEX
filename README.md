# 🧠 Lex – Your Personal, Local-First, Sarcastic AI Assistant

Lex is your on-PC digital assistant that doesn’t spy on you, doesn’t eat your FPS, and doesn’t give a damn if you asked nicely.  
Think: **Jarvis**, if he chain-smoked sarcasm and refused to use the cloud without permission.

---

## ⚙️ What It Is

Lex is a **modular, locally-running AI assistant** designed to:
- Stay offline unless *you* say otherwise
- Be extended easily through plugin-style commands
- Talk back with sarcastic, human-like sass
- Automate basic crap so you don’t forget to drink water (again)

---

## ✅ What Actually Works Right Now

### Functional Core:
- ✅ Modular plugin loader (via `dispatcher.py`)
- ✅ Async command processing (non-blocking CLI loop)
- ✅ Config loader with default injection (`settings.json`)
- ✅ Fully offline (unless using `define`, which pings an API)

### Plugin Commands (Some working):
- ✅ `remind me in X minutes to Y` (with persistence + cancel/list)
- ✅ `open notepad`, `search for cats` (real app and browser launches)
- ✅ `kill discord` (taskkill whitelist-safe)
- ✅ `generate password`, `generate uuid`
- ✅ `flip a coin`, `roast me`, `compliment me`
- ✅ `define <word>` (real API-based)
- ✅ `weather` (mocked for now)
- ✅ `vault` with AES encryption, master password, and CRUD ops

---

## 🛣 Roadmap

### 🚧 Short-Term (in progress / queued)
- [ ] Voice input via Whisper or speech_recognition
- [ ] Text-to-speech output (pyttsx3, ElevenLabs optional)
- [ ] Plugin hot reloading (no restarts for new modules)
- [ ] Debug dashboard or CLI monitor
- [ ] Cross-platform support (Linux/macOS compatibility)

### 🧠 Future Ideas
- [ ] Routine learning (suggest recurring tasks based on behavior)
- [ ] Context tracking (multi-step conversation memory)
- [ ] Plugin marketplace or repo sync
- [ ] Sarcasm tone slider in `settings.json` (because chaos)

---

## 📂 Folder Structure
