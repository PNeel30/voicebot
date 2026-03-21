from fastapi import FastAPI, File, UploadFile, Form
import shutil, uuid, os
from app.stt import transcribe
from app.utils import detect_language, translate_text_stub
from app.rag import run_rag
from app.tts import synthesize
from app.memory import push_user_turn, get_user_memory

app = FastAPI()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/voice-query")
async def voice_query(user_id: str = Form(...), file: UploadFile = File(...), language_hint: str = Form(None)):
    fname = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = transcribe(path, language_hint=language_hint)
    if not text:
        return {"error": "Could not transcribe audio."}

    lang = detect_language(text)
    memory = get_user_memory(user_id)
    memory_context = "\n".join(memory) if memory else None

    rag_result = run_rag(text, user_lang=lang)
    answer = rag_result.get("answer", "")
    confidence = rag_result.get("confidence", 0.0)
    low_conf = rag_result.get("low_confidence", False)

    push_user_turn(user_id, f"U: {text}")
    push_user_turn(user_id, f"B: {answer}")

    tts_file = synthesize(answer, lang_code=lang)
    try: os.remove(path)
    except Exception: pass

    return {"transcript": text, "answer_text": answer, "confidence": confidence, "low_confidence": low_conf, "tts_audio_path": tts_file}
