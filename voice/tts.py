import requests
import pyttsx3


class TTS:
    def __init__(self, settings: dict):
        self.settings = settings
        self.engine = None
        if self.settings.get("tts_engine", "pyttsx3") == "pyttsx3":
            try:
                self.engine = pyttsx3.init()
                name = self.settings.get("voice_name")
                if name:
                    for voice in self.engine.getProperty("voices"):
                        if name.lower() in voice.name.lower():
                            self.engine.setProperty("voice", voice.id)
                            break
                rate = self.settings.get("voice_rate")
                if rate:
                    self.engine.setProperty("rate", rate)
                pitch = self.settings.get("voice_pitch")
                if pitch is not None:
                    try:
                        self.engine.setProperty("pitch", pitch)
                    except Exception:
                        pass
            except Exception as e:
                print(f"[Lex] pyttsx3 error: {e}")

    def speak(self, text: str) -> None:
        """Speak the given text using the configured engine."""
        if self.settings.get("use_cloud") and self.settings.get("tts_engine") == "elevenlabs":
            api_key = self.settings.get("elevenlabs_api_key")
            if not api_key:
                print("[Lex] ElevenLabs API key missing")
                return
            try:
                requests.post(
                    "https://api.elevenlabs.io/v1/text-to-speech",
                    headers={"xi-api-key": api_key},
                    json={"text": text},
                    timeout=10,
                )
            except Exception as e:
                print(f"[Lex] ElevenLabs error: {e}")
        elif self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
