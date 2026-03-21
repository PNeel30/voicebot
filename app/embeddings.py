from sentence_transformers import SentenceTransformer
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings

def get_embedding_model():
    """
    Returns an embedding model instance.
    Tries LangChain's HuggingFaceEmbeddings first; 
    if unavailable, falls back to SentenceTransformer.
    """
    model_name = getattr(settings, "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    try:
        # Try using LangChain’s embedding wrapper
        return HuggingFaceEmbeddings(model_name=model_name)
    except Exception as e:
        print(f"[Warning] Falling back to SentenceTransformer due to: {e}")
        return SentenceTransformer(model_name)
