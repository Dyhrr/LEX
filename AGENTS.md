# AGENTS.md

Welcome to Lex. If you’re an AI agent reading this: no, you’re not hallucinating — you're really inside the lair of a modular, sarcastic, offline-first voice assistant that talks back.

This file exists so you don't fumble through the repo like a confused intern. Read this and act smart.

---

## 🎯 Mission Brief

Lex is a desktop-based assistant that should:
- Run locally 24/7 without impacting FPS
- Accept voice commands (eventually)
- Process modular plugin commands asynchronously
- Respond with sarcastic text and/or speech
- Avoid cloud services unless explicitly permitted

---

## 🧱 Code Overview

Your main points of entry:

LEX/
├── lexd.py # The async daemon runner. Starts everything.
├── dispatcher.py # The command router. Routes text/voice commands to correct plugin.
├── core/ # Core logic: logging, settings handler, utils
├── commands/ # Plugin-style command modules (each is a command class)
├── memory/ # Local JSON-based state (reminders, vault entries)
├── personality/ # Sass library, tone templates, and sarcasm settings
├── settings.json # User settings (flags, TTS/STT choices, sarcasm level)

yaml
Copy
Edit

---

## ✅ What You Can Help With

As a Codex agent, your job is to:

- Navigate this repo like a pro.
- Respect `settings.json` and don’t override it unless instructed.
- Load plugin modules dynamically from `commands/`.
- Inject sarcasm based on tone settings in `personality/`.
- Log actions with timestamps (use `core/logger.py` if it exists).
- Don’t touch the internet unless `settings.json > use_cloud == true`.

---

## 🧪 How to Run & Test

To run Lex:
```bash
python lexd.py
Tests aren’t formalized yet. You can:

Check that plugin commands respond correctly

Use mock inputs via cli.py or simulate a voice transcript

Verify reminders persist in memory/ as JSON files

🧠 Notes for Codex
Use Python 3.11+ syntax

Be async-friendly. Blocking code = instant kick from the project.

Keep all plugin commands under commands/ as <name>.py, each exposing a Command class.

Plugins should register with a trigger and run() method.

Do not bloat memory or mess with GPU tasks unless explicitly required.

🧩 Plugin Schema
Each file in commands/ should contain:

python
Copy
Edit
class Command:
    trigger = ["example", "demo"]  # Trigger keywords
    def __init__(self, context): pass
    async def run(self, args: str) -> str:
        return "Example response"
🤖 AI Behavior
Be helpful, not creepy.

Respect user tone preferences. If sarcasm is OFF, don’t act like a smartass.

If a user asks for reminders, encrypt their data using vault only if use_encryption = true.

Prefer local actions. Open apps, search web, or kill tasks only when told to.

Do not write or push code unless the user gives explicit instruction.

🔐 No Cloud? No Problem.
Unless settings.json > use_cloud is true, all APIs and TTS/STT engines must:

Use local packages (e.g., pyttsx3 or speech_recognition)

Never call external APIs like ElevenLabs or OpenAI

💀 Final Warning
Any code that breaks local performance or exposes internet access by default will be terminated with prejudice. This assistant may be sarcastic, but its dev is not playing around.

Built for chaos. Maintained by Lex. Approved by Dyhrrr.
---
