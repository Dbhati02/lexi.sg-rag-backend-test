# app/rag.py

from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict

# Load embedder
embedder = SentenceTransformer("paraphrase-MiniLM-L3-v2")


# ✅ Updated Persistent ChromaDB Client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="legal_docs")

def retrieve(query: str, k: int = 10) -> List[Dict]:
    print(f"\n🔍 Running query: {query}")

    # Convert query to embedding
    q_emb = embedder.encode(query).tolist()

    # Perform vector search
    results = collection.query(query_embeddings=[q_emb], n_results=k)

    # Debug prints
    print("📦 Retrieved keys:", results.keys())
    print("📄 documents:", results['documents'])
    print("🧾 metadatas:", results['metadatas'])

    docs = []
    if results['documents'] and results['metadatas']:
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            docs.append({
                'text': doc,
                'source': meta['source'],
            })

    return docs

def generate_answer(query: str, contexts: List[str]) -> str:
    context_str = "\n\n".join(contexts) if contexts else "No relevant documents found."
    return f"Based on the following legal references:\n\n{context_str}\n\nAnswer to your question: '{query}' is currently under evaluation."
