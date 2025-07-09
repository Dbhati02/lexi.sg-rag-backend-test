# Lexi RAG Backend (FastAPI + ChromaDB)

This project implements a Retrieval-Augmented Generation (RAG) backend using FastAPI, Sentence Transformers, and ChromaDB to answer legal queries and return supporting citations.

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Dbhati02/lexi.sg-rag-backend-test.git
cd lexi.sg-rag-backend-test

## Set up a virtual environment

python -m venv venv
.\venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On Mac/Linux

 ##Install dependencies
pip install -r requirements.txt

##Document Ingestion (One-Time Step)
python scripts/ingest.py
##Run the Backend Server
uvicorn app.main:app --reload --port 8000

http://localhost:8000/docs

##input
{
  "query": "What happens if a vehicle involved in an accident doesn't have a valid permit?"
}

##output
{
  "answer": "Based on the following legal references:\n\n... \n\nAnswer to your question: 'What happens if a vehicle involved in an accident doesn't have a valid permit?' is currently under evaluation.",
  "citations": [
    {
      "text": "The insurance company cannot be exonerated from liability solely due to the absence of a permit.",
      "source": "insurance_liability_sample.docx"
    }
  ]
}
