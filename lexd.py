# Main daemon entry

import asyncio
import argparse
import logging
from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher
from voice.recognizer import transcribe
from voice.tts import TTS
from core.logger import get_logger, set_log_level


logger = get_logger()


async def main() -> None:
    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})
    speaker = TTS(settings) if settings.get("voice_output") else None

    logger.info("Starting daemon loop...")
    while True:
        if settings.get("voice_input"):
            try:
                # Pass optional duration if supported, fallback to default
                cmd = await transcribe(settings.get("transcription_duration", 5))
                logger.info("> %s", cmd)
                if not cmd:
                    cmd = (await asyncio.to_thread(input, "> ")).strip()
            except Exception as e:
                logger.error("Voice input error: %s", e)
                cmd = (await asyncio.to_thread(input, "> ")).strip()
        else:
            cmd = (await asyncio.to_thread(input, "> ")).strip()
        if cmd:
            logger.info("Command received: %s", cmd)
            response = await dispatcher.dispatch(cmd)
            if response:
                logger.info("Response: %s", response)
                if speaker:
                    await speaker.speak(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lex daemon")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings")
    args = parser.parse_args()

    if args.verbose:
        set_log_level(logging.DEBUG)
    elif args.quiet:
        set_log_level(logging.WARNING)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down.")
