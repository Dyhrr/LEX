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
LEX/
├── lexd.py # Main async loop
├── dispatcher.py # Plugin command router
├── settings.json # Global config
├── core/ # Core settings/utils
├── commands/ # Your plugin modules
├── memory/ # Persistent storage (reminders, vault)
├── personality/ # Tone files, sass library
---

💡 Design Philosophy
Lex is:

Not cloud-bound

Not polite by default

Not eating 1GB of RAM to tell you what time it is

He’s meant to be:

Expandable

Sarcastically helpful

Dumb enough to stay local, smart enough to feel personal

🔒 Licensing
MIT License.
No analytics. No telemetry. Just you, your PC, and a personality-injected assistant with attitude.

🐢 Credits
Made by Dyhrrr — the kind of dev who sleeps on the floor but builds tools better than your average SaaS startup.

“Built to automate my life, so I can keep ignoring it.”


