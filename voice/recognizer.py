import os
import speech_recognition as sr


def transcribe(timeout: int | None = None) -> str:
    """Listen from the microphone and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=timeout)
    try:
        return recognizer.recognize_sphinx(audio)
    except (sr.UnknownValueError, sr.RequestError):
        pass
    # Fallback to whisper if installed and speech_recognition failed
    try:
        import whisper
        model = whisper.load_model("base")
        with open("_tmp.wav", "wb") as fh:
            fh.write(audio.get_wav_data())
        result = model.transcribe("_tmp.wav")
        os.remove("_tmp.wav")
        return result.get("text", "").strip()
    except Exception:
        return ""
