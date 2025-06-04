# 🧠 Lex – Your Personal, Local-First, Sarcastic AI Assistant

Lex is your on-PC digital assistant that doesn’t spy on you, doesn’t eat your RAM for breakfast, and won’t apologize every time it fails (because it probably meant to).  
Think: **Jarvis** if he was coded by a sleep-deprived gamer with control issues and a mild god complex.

---

## ⚙️ What It Is

Lex is a **modular, low-resource, always-on AI assistant** built to:
- Run **100% locally** (no cloud required unless you say so)
- Do **actual useful shit** like reminders, app launches, password storage
- Be **expandable** with drop-in command modules (plugins)
- Talk to you like a roommate who’s too smart for their own good

---

## 💡 Features

✅ Natural command detection (no slash commands, just talk to it)  
✅ Async reminder system (multi-tasking, persistent across reboots)  
✅ AES-encrypted password vault (master password protected)  
✅ Dictionary definitions, password generator, coinflips, insults  
✅ App launcher + Google search built-in  
✅ Safe Windows process killer (kill Discord, not your whole system)  
✅ Sarcastic fallback responses if you fail to make sense  
✅ Fully modular plugin system with hot reload support (soon)

---

## 🛣 Roadmap (Short-Term)

- [x] All base plugins functional
- [x] Persistent reminders with human cancelation
- [x] Vault with real encryption (Fernet)
- [x] Voice-safe dispatcher with async CLI
- [ ] Speech input/output support (Whisper STT, ElevenLabs TTS)
- [ ] Context-aware responses + memory system
- [ ] Plugin hot reload support
- [ ] Smart scheduler (daily routines, adaptive habits)
- [ ] Developer UI / debug dashboard

---

## 🧱 Tech Stack

- **Language**: Python 3.10+
- **Core**: `asyncio`, `cryptography`, `requests`
- **Optional**: `pycaw`, `speech_recognition`, `torch` (for future voice stuff)
- **File structure**:
