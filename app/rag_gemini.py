import os, json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment or .env file")
genai.configure(api_key=GEMINI_API_KEY)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/sample_corpus.json")
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(os.getcwd(), "sample_corpus.json")

def run_rag(question: str, user_lang: str = "en", min_conf: float = 0.15, top_k: int = 3):
    # Reload corpus
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            all_corpus = json.load(f)
    except Exception:
        all_corpus = []
    
    # Filter by language
    if user_lang and user_lang != "en":
        corpus = [doc for doc in all_corpus if doc.get("language") == user_lang]
        if not corpus:
            corpus = all_corpus
    else:
        corpus = all_corpus
    
    if not corpus:
        return {"answer": "No corpus data found.", "context": "", "confidence": 0.0}
    
    # Use Gemini embeddings for better multilingual support
    try:
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=question,
            task_type="retrieval_query"
        )["embedding"]
        
        # Get embeddings for all documents
        doc_embeddings = []
        for doc in corpus:
            emb = genai.embed_content(
                model="models/text-embedding-004",
                content=doc.get("content", ""),
                task_type="retrieval_document"
            )["embedding"]
            doc_embeddings.append(emb)
        
        # Calculate cosine similarity
        import numpy as np
        scores = []
        for doc_emb in doc_embeddings:
            similarity = np.dot(query_embedding, doc_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            scores.append(similarity)
        
        # Get top k
        top_indices = np.argsort(scores)[-top_k:][::-1]
        top_scores = [scores[i] for i in top_indices]
        confidence = float(np.mean(top_scores))
        
        context = "\n\n".join([corpus[i]["content"] for i in top_indices])
        
        print(f"DEBUG: Question: {question}")
        print(f"DEBUG: Confidence: {confidence:.3f}")
        print(f"DEBUG: Top scores: {[f'{s:.3f}' for s in top_scores]}")
        print(f"DEBUG: Top docs: {[corpus[i].get('title', '')[:50] for i in top_indices]}")
        
    except Exception as e:
        print(f"DEBUG: Embedding failed: {str(e)[:200]}")
        # Fallback to simple text matching
        context = "\n\n".join([doc.get("content", "") for doc in corpus[:top_k]])
        confidence = 0.5
    
    if confidence < min_conf or not context.strip():
        return {"answer": "Mujhe is vishay mein jaankari nahi hai.", "context": "", "confidence": round(confidence, 3)}
    
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the provided context in the same language as the question.

Context:
{context}

Question: {question}

Answer in {user_lang if user_lang == 'hi' else 'the same language'}:"""
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        return {"answer": text, "context": context, "confidence": round(confidence, 3)}
    except Exception as e:
        print(f"DEBUG: LLM failed, using direct context: {str(e)[:100]}")
        # Return first context directly (already correct answer)
        return {"answer": context.split("\n\n")[0], "context": context, "confidence": round(confidence, 3)}

if __name__ == "__main__":
    print("RAG-Gemini session started")
    while True:
        q = input("\nQuestion: ").strip()
        if not q or q.lower() in {"exit", "quit"}:
            break
        res = run_rag(q, user_lang="hi")
        print(f"\nAnswer: {res['answer']}\nConfidence: {res['confidence']}\n")
