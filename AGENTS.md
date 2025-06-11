# AGENTS.md

Welcome to Lex. If you're an AI agent or Codex reviewer, this file exists to make sure you know how to operate inside this repo **without wasting time or being useless**. No fluff, just expectations.

---

## 🎯 Mission Brief

Lex is a modular, local-first desktop assistant that:
- Runs 24/7 with minimal system impact (gaming-safe)
- Accepts voice commands and runs modular plugin commands asynchronously
- Responds with text and optionally speech
- Uses sarcasm **only** if the user enables it in `settings.json`
- Avoids all cloud-based actions unless explicitly allowed by user

You are here to help review and improve Lex like a **real developer and QA tester**, not a clueless intern.

---

## 🧱 Code Overview

```
LEX/
├── lexd.py           # The async daemon runner (entry point)
├── dispatcher.py     # Routes text/voice input to correct plugin
├── core/             # Logging, config parsing, utility functions
├── commands/         # Plugin command modules (1 class per file)
├── memory/           # JSON-based vaults, reminders, and state
├── personality/      # Response tone templates, sass configs
├── settings.json     # Master config file, local-only settings
```

---

## 🤖 Codex Agent Instructions

You are expected to:
- Read the repo like a **senior developer**
- Load plugin modules from `commands/`
- Honor `settings.json` settings at all times
- NEVER use online APIs unless `use_cloud` is explicitly set true
- Inject sarcasm **only** if sarcasm is enabled
- Avoid blocking or sync code in any async loop
- Use Python 3.11+ and async syntax for all contributions

---

## 🧪 Review Expectations

When reviewing or generating code:
- Be **ruthlessly honest**. Don’t sugarcoat broken logic
- Review like the project ships tomorrow
- Always prefer clarity and maintainability over clever hacks

Use this structure when giving feedback:
1. **Code Logic Issues**: List fragile, unclear, or inefficient logic
2. **UX/Flow Issues**: Confusing flows, bad defaults, annoying usage patterns
3. **Suggested Fixes**: Concrete changes that improve the above
4. **Usability Score (0–10)**: Based on logic, structure, and clarity

Example Prompt:
> "Review `dispatcher.py` like it's going live tomorrow. Tell me what’s bad, unclear, overcomplicated, or fragile. Suggest specific rewrites."

---

## 🧩 Plugin Schema

Each command plugin must:
```python
class Command:
    trigger = ["example"]
    def __init__(self, context): pass
    async def run(self, args: str) -> str:
        return "Handled."
```

---

## 🔐 Security & Local Behavior
- Do not call external APIs unless `use_cloud` is set
- Encrypt memory data only if `use_encryption = true`
- Do not increase GPU load unless explicitly asked

---

## 🛑 Final Rule
Any code that breaks performance, overrides user settings, or assumes cloud access **will be rejected**. This assistant is meant to work **locally, efficiently, and under the user’s full control.**

That includes you.

Built for creators. Protected by Lex. Approved by Dyhrrr.
