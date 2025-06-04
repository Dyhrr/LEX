import os
import asyncio
from tempfile import NamedTemporaryFile
import speech_recognition as sr


_whisper_model = None


async def _get_whisper_model():
    """Load and cache the Whisper model."""
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            _whisper_model = await asyncio.to_thread(whisper.load_model, "base")
        except Exception:
            _whisper_model = False  # Flag to avoid retrying
    return _whisper_model


async def transcribe(timeout: int | None = None) -> str:
    """Listen from the microphone and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = await asyncio.to_thread(
                recognizer.listen, source, timeout=timeout
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        return recognizer.recognize_sphinx(audio)
    except (sr.UnknownValueError, sr.RequestError):
        pass

    model = await _get_whisper_model()
    if not model:
        return ""

    tmp_file = NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp_file.name
    try:
        tmp_file.write(audio.get_wav_data())
        tmp_file.close()
        result = await asyncio.to_thread(model.transcribe, tmp_path)
        return result.get("text", "").strip()
    except Exception:
        return ""
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
