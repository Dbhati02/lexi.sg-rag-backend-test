from fastapi import FastAPI
from app.models import QueryRequest, QueryResponse, Citation
from app.rag import retrieve, generate_answer

app = FastAPI(title="Lexi RAG Backend")

@app.post("/query", response_model=QueryResponse)
def query_route(req: QueryRequest):
    hits = retrieve(req.query)
    snippets = [h['text'] for h in hits]
    answer = generate_answer(req.query, snippets)
    citations = [Citation(text=h['text'], source=h['source']) for h in hits]
    return QueryResponse(answer=answer, citations=citations)
