# Plugin Overview

A quick reference for the command plugins shipped with Lex. Triggers are the words
that invoke each plugin. Many modules are still placeholders awaiting
implementation.

| Plugin | Triggers | Description |
|-------|----------|-------------|
| cleanup.py | `cleanup` | Remove `.tmp` files or clear Python caches. |
| clipboard.py | `clipboard` | Maintain a simple clipboard history (add, show, paste, clear). |
| codeassist.py | `codeassist` | Return handy Python code snippets for common tasks. |
| collab.py | `collab` | Share a folder over HTTP to quickly collaborate. |
| define.py | `define` | Look up word definitions using a web API when cloud access is allowed. |
| email_summary.py | `email_summary` | Summarize unread emails from a local mailbox. |
| features.py | `features`, `missing features` | List potential new features from a JSON suggestions file. |
| gaming.py | `game`, `gaming` | Roll dice or flip a coin. |
| health.py | `health`, `stats` | Report basic CPU, RAM and disk usage. |
| help.py | `help` | List all available command triggers. |
| history.py | `history`, `context` | Show recent command history and results. |
| info.py | `info` | Display loaded commands and current settings. |
| doctor.py | `doctor` | Run diagnostics to check your Lex setup. |
| knowledge.py | `knowledge` | Search local documentation for matching lines. |
| learn.py | `learn`, `teach` | Teach Lex new phrases that map to commands. |
| notes.py | `notes`, `note` | Store short notes locally. |
| notify.py | `notify` | Send desktop notifications and list recent ones. |
| personality.py | `personality` | Get or set sarcasm level. |
| ping.py | `ping`, `are you alive` | Respond with a simple "Pong" message. |
| pingback.py | `pingback` | Check if a host is reachable via `ping`. |
| proactive.py | `proactive` | Battery alerts and scheduled command triggers. |
| profile.py | `profile` | Manage a simple local profile (`show`, `set`, `delete`). |
| remind.py | `remind` | Store and list reminders. |
| schedule.py | `schedule` | Manage dated events in a small local schedule. |
| search.py | `search`, `find`, `locate` | Search files from a local index. |
| secdash.py | `secdash` | Show active network connections and kill by PID. |
| smarthome.py | `smarthome` | Control lights, thermostat, or scenes via Home Assistant. |
| system.py | `system` | Show basic system information. |
| tone.py | `tone` | Adjust voice name, rate and pitch. |
| tools.py | `tools` | Generate UUIDs or random passwords. |
| translate.py | `translate` | Translate text using a small offline dictionary or cloud API. |
| vault.py | `vault` | Store or retrieve key/value pairs, optionally encrypted. |
| wakeword.py | `wakeword` | Listen for custom wake words to trigger commands. |
| weather.py | `weather` | Return a weather report (cloud or local). |
| hotkey.py | `hotkey` | Register global hotkeys that trigger Lex commands. |
| hud.py | `hud` | Show a small CPU and memory usage overlay window. |
| workflow.py | `workflow` | Create and execute multi-step command workflows. |

## Textual UI

Launch `lexui.py` for a simple text-based interface. Use the optional
`--sidebar` flag to list available command triggers in a side panel.

