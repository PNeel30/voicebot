import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma  # Updated import
from app.embeddings import get_embedding_model
from app.config import settings

# Ensure the Chroma directory exists
os.makedirs(settings.CHROMA_DIR, exist_ok=True)

def ingest_json(json_path: str):
    # Load the input JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    docs = []
    for item in items:
        sid = item.get("scheme_id") or item.get("id") or ""
        lang = item.get("language") or item.get("lang") or "en"
        title = item.get("title") or ""
        content = item.get("content") or ""

        text = f"{title}\n\n{content}".strip()
        if not text:
            continue

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "id": sid,
                    "lang": lang,
                    "source": os.path.basename(json_path),
                },
            )
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    embedding_model = get_embedding_model()

    # New Chroma initialization - no need for .persist()
    vectordb = Chroma(
        collection_name="voicebot_docs",
        embedding_function=embedding_model,
        persist_directory=settings.CHROMA_DIR,
    )

    vectordb.add_documents(split_docs)

    print(f"[INFO] Ingestion complete. {len(split_docs)} chunks stored in {settings.CHROMA_DIR}")

    return vectordb


if __name__ == "__main__":
    json_file = os.path.join(os.path.dirname(__file__), "../data/sample_corpus.json")
    ingest_json(json_file)
