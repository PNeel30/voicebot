# Multilingual Vernacular Voicebot with RAG

A voice-based query system for rural/semi-urban India supporting Hindi, Tamil, Bengali, and other Indian languages.

## Features

- **Speech-to-Text**: Whisper large-v2 with forced Hindi language detection
- **RAG Pipeline**: Gemini embeddings API (text-embedding-004) with cosine similarity
- **Multilingual Support**: Hindi, Tamil, Bengali, English
- **Text-to-Speech**: Google TTS for voice responses
- **Confidence Scoring**: Prevents hallucinations with threshold-based responses
- **Language Filtering**: Filters corpus by language before retrieval

## Architecture

```
Audio Input → STT (Whisper large-v2) → Query Embedding (Gemini API)
                                              ↓
                                    Cosine Similarity Search
                                              ↓
                                    Top-K Context Retrieval
                                              ↓
                            LLM (Gemini 1.5 Flash) → TTS → Audio Output
```

## Setup

### Local Development

```powershell
# Create virtual environment
python -m venv hello
.\hello\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Create .env file with:
# GEMINI_API_KEY=your_key_here

# Run app (no index building required - embeddings generated on-the-fly)
streamlit run streamlit_app.py
```

### Docker

```powershell
# Build image
docker build -t voicebot .

# Run container
docker run -p 8501:8501 --env-file .env voicebot
```

## Usage

1. Upload audio file (WAV/MP3/M4A)
2. Select language (optional, auto-detects)
3. View transcript and retrieved context
4. Get generated response with confidence score
5. Listen to audio response

## Configuration

Edit `app/config.py`:

- `STT_MODEL`: Whisper model size (default: large-v2)
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `RETRIEVER_CONFIDENCE_THRESHOLD`: Minimum retrieval score (default: 0.15)
- `TOP_K_RETRIEVAL`: Number of documents to retrieve (default: 3)

## API Endpoints

FastAPI server available at `app/main.py`:

```bash
uvicorn app.main:app --reload
```

- `POST /query`: Text query
- `POST /voice-query`: Audio file upload

## Model Choices

- **STT**: Whisper large-v2 with forced Hindi language (prevents Urdu script)
- **Embeddings**: Gemini text-embedding-004 (superior Hindi understanding)
- **LLM**: Google Gemini 1.5 Flash Latest
- **TTS**: Google TTS (supports Hindi, Bengali, Tamil)

## Anti-Hallucination Strategy

1. **Retrieval Confidence**: Cosine similarity score from Gemini embeddings
2. **Language Filtering**: Pre-filters corpus by user language before retrieval
3. **Fallback Response**: "Mujhe is vishay mein jaankari nahi hai" when confidence < 0.15
4. **Context Grounding**: LLM instructed to use only provided context
5. **Direct Context Fallback**: Returns top retrieved document if LLM fails

## Project Structure

```
Voicebot/
├── app/
│   ├── config.py          # Configuration
│   ├── stt.py             # Speech-to-text (Whisper)
│   ├── rag_gemini.py      # RAG with Gemini embeddings API
│   ├── tts.py             # Text-to-speech (gTTS)
│   └── main.py            # FastAPI server (optional)
├── data/
│   └── sample_corpus.json # Knowledge base
├── streamlit_app.py       # Web UI
├── requirements.txt
├── Dockerfile
└── README.md
```

## Adding New Data

Add entries to `data/sample_corpus.json`:

```json
{
  "id": "new_scheme",
  "language": "hi",
  "category": "agriculture",
  "title": "New Scheme",
  "content": "Scheme details in Hindi..."
}
```

No rebuild needed - embeddings are generated on-the-fly using Gemini API.

## License

MIT
