"""Translate short text between languages."""

import asyncio


OFFLINE_DICT = {
    ("hello", "es"): "hola",
    ("goodbye", "es"): "adios",
    ("hola", "en"): "hello",
}


class Command:
    description = "Translate text using a small offline dictionary or cloud API."
    trigger = ["translate"]

    def __init__(self, context):
        self.context = context
        self.settings = context.get("settings", {})

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if len(tokens) < 2:
            return "[Lex] Use 'translate <lang> <text>'."

        lang = tokens[0]
        text = " ".join(tokens[1:])

        if not text:
            return "[Lex] Nothing to translate."

        if not self.settings.get("use_cloud"):
            match = OFFLINE_DICT.get((text.lower(), lang))
            if match:
                return match
            return (
                "[Lex] Offline dictionary is limited. Enable cloud for more langu" "ages."
            )

        try:
            from deep_translator import GoogleTranslator
        except Exception as e:
            return f"[Lex] Translation unavailable: {e}"

        try:
            translator = GoogleTranslator(source="auto", target=lang)
            return await asyncio.to_thread(translator.translate, text)
        except Exception as e:
            return f"[Lex] Translation failed: {e}"
