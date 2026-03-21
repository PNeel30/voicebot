from langdetect import detect_langs

def detect_language(text: str) -> str:
    try:
        langs = detect_langs(text)
        return langs[0].lang if langs else "en"
    except Exception:
        return "en"

def translate_text_stub(text: str, target_lang: str = "en") -> str:
    if not text.strip():
        return ""
    return text
