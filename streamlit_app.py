import streamlit as st, tempfile, os
from app.stt import transcribe
from app.utils import detect_language
from app.rag_gemini import run_rag
from app.tts import synthesize

st.set_page_config(page_title="Vernacular Voicebot", layout="centered")
st.title("Vernacular Voicebot")

user_id = st.text_input("User ID", value="user_1")
language_hint = st.text_input("Language Hint (optional)", value="")
uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp_path = tmp.name
        tmp.write(uploaded_file.read())

    with st.spinner("Transcribing..."):
        transcript = transcribe(tmp_path, language_hint or None)

    st.subheader("Transcript")
    st.write(transcript or "Could not detect speech.")

    lang = detect_language(transcript or "")
    st.write(f"Detected Language: {lang}")

    with st.spinner("Generating AI response..."):
        result = run_rag(transcript, user_lang=lang)

    answer = result.get("answer", "")
    st.subheader("AI Answer")
    st.write(answer or "No response generated.")

    with st.spinner("Converting to speech..."):
        tts_path = synthesize(answer, lang_code=lang)

    if os.path.exists(tts_path):
        st.audio(tts_path, format="audio/mp3")
    try: os.remove(tmp_path)
    except: pass
