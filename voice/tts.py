import asyncio
import sys
import os
import tempfile
import requests
import simpleaudio
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
                if pitch is not None and sys.platform != "win32":
                    try:
                        self.engine.setProperty("pitch", pitch)
                    except Exception:
                        pass
            except Exception as e:
                print(f"[Lex] pyttsx3 error: {e}")

    async def speak(self, text: str) -> None:
        """Speak the given text using the configured engine."""
        if self.settings.get("use_cloud") and self.settings.get("tts_engine") == "elevenlabs":
            api_key = self.settings.get("elevenlabs_api_key")
            voice_id = self.settings.get("elevenlabs_voice_id")
            if not api_key or not voice_id:
                print("[Lex] ElevenLabs API key or voice ID missing")
                return
            try:
                response = await asyncio.to_thread(
                    requests.post,
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
                    headers={
                        "xi-api-key": api_key,
                        "Content-Type": "application/json",
                        "Accept": "audio/wav",
                    },
                    json={"text": text},
                    timeout=10,
                )
                if response.ok:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(response.content)
                        tmp_path = tmp.name
                    wave_obj = await asyncio.to_thread(simpleaudio.WaveObject.from_wave_file, tmp_path)
                    play_obj = wave_obj.play()
                    await asyncio.to_thread(play_obj.wait_done)
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
                else:
                    print(f"[Lex] ElevenLabs error: {response.status_code}")
            except Exception as e:
                print(f"[Lex] ElevenLabs error: {e}")
        elif self.engine:
            await asyncio.to_thread(self._speak_pyttsx3, text)

    def _speak_pyttsx3(self, text: str) -> None:
        """Helper to run pyttsx3 in a thread."""
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
