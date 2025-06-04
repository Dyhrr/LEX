# Main daemon entry

import asyncio
from core.settings import load_settings
from dispatcher import Dispatcher
from voice.recognizer import transcribe
from voice.tts import TTS


async def main() -> None:
    settings = load_settings()
    dispatcher = Dispatcher({"settings": settings})
    speaker = TTS(settings) if settings.get("voice_output") else None

    print("[Lex] Starting daemon loop...")
    while True:
        if settings.get("voice_input"):
            try:
                cmd = await asyncio.to_thread(transcribe)
                print(f"> {cmd}")
            except Exception as e:
                print(f"[Lex] Voice input error: {e}")
                cmd = (await asyncio.to_thread(input, "> ")).strip()
        else:
            cmd = (await asyncio.to_thread(input, "> ")).strip()
        if cmd:
            response = await dispatcher.dispatch(cmd)
            if response:
                print(response)
                if speaker:
                    await speaker.speak(response)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Lex] Shutting down.")
