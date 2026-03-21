from faster_whisper import WhisperModel
import os
_model = None

def get_model():
    global _model
    if _model is None:
        model_size = os.getenv("STT_MODEL", "small")
        try:
            _model = WhisperModel(model_size, device="cpu", compute_type="float32")
        except Exception:
            _model = WhisperModel(model_size, device="cpu")
    return _model

def transcribe(audio_path: str, language_hint=None):
    model = get_model()
    segments, _ = model.transcribe(audio_path, beam_size=5, language=language_hint, word_timestamps=False)
    text = " ".join([segment.text for segment in segments])
    return text.strip()
