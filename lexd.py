# Main daemon entry

import asyncio
from core.settings import load_settings
from dispatcher import Dispatcher


async def main() -> None:
    settings = load_settings()
    dispatcher = Dispatcher({"settings": settings})

    print("[Lex] Starting daemon loop...")
    while True:
        cmd = input("> ").strip()
        if cmd:
            response = await dispatcher.dispatch(cmd)
            if response:
                print(response)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Lex] Shutting down.")
