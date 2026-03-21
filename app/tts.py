import tempfile, os
_FORCE_COQUI = os.getenv("USE_COQUI", "0") == "1"
_TTS_COQUI_AVAILABLE = False
if _FORCE_COQUI:
    try:
        from TTS.api import TTS
        _TTS_COQUI_AVAILABLE = True
    except Exception:
        _TTS_COQUI_AVAILABLE = False

if not _TTS_COQUI_AVAILABLE:
    from gtts import gTTS
    _USE_COQUI = False
else:
    _USE_COQUI = True

_tts = None

def get_tts():
    global _tts
    if _tts is None and _USE_COQUI:
        model_name = os.getenv("TTS_MODEL", "tts_models/multilingual/multi-dataset/your-model")
        _tts = TTS(model_name=model_name)
    return _tts

def synthesize(text: str, lang_code="hi", speaker=None):
    tmp_ext = ".wav" if _USE_COQUI else ".mp3"
    tmpfile = tempfile.NamedTemporaryFile(suffix=tmp_ext, delete=False)
    out_path = tmpfile.name
    if _USE_COQUI:
        tts = get_tts()
        tts.tts_to_file(text=text, speaker=speaker, language=lang_code, file_path=out_path)
    else:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(out_path)
    return out_path
