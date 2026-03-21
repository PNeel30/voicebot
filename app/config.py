import os
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    STT_MODEL: str = os.getenv("STT_MODEL", "small")
    TTS_MODEL: str = os.getenv("TTS_MODEL", "tts_models/multilingual/multi-dataset/your-model")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    RETRIEVER_TOPK: int = int(os.getenv("RETRIEVER_TOPK", "5"))
    MIN_SIMILARITY: float = float(os.getenv("MIN_SIMILARITY", "0.27"))
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/tmp/uploads")

    class Config:
        env_file = ".env"

settings = Settings()
