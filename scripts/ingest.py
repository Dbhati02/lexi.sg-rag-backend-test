# scripts/ingest.py

import os
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from docx import Document
import chromadb

def load_texts(doc_dir="docs"):
    texts = []
    for fname in os.listdir(doc_dir):
        if fname.startswith("~$"):  # Skip temp Word files
            continue
        path = os.path.join(doc_dir, fname)
        text = ""

        if fname.endswith('.pdf'):
            try:
                reader = PdfReader(path)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            except Exception as e:
                print(f"❌ Error reading PDF {fname}: {e}")

        elif fname.endswith('.docx'):
            try:
                doc = Document(path)
                text = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"❌ Error reading DOCX {fname}: {e}")
        else:
            continue

        print(f"📄 Loaded: {fname} ({len(text)} characters)")
        texts.append((fname, text))
    return texts

def chunk_and_index(texts, collection):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embedder = SentenceTransformer("paraphrase-MiniLM-L3-v2")


    for fname, text in texts:
        chunks = splitter.split_text(text)
        print(f"🔹 {fname} split into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": fname, "chunk_id": i}],
                ids=[f"{fname}-{i}"]
            )

def main():
    print("⚙️ Starting ingestion...")

    # ✅ Updated Chroma Client (Persistent)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="legal_docs")

    texts = load_texts()
    if not texts:
        print("⚠️ No valid documents found in 'docs/' folder.")
        return

    chunk_and_index(texts, collection)
    print("✅ Ingestion complete and saved.")

if __name__ == "__main__":
    main()
