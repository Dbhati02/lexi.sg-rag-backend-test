from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class Citation(BaseModel):
    text: str
    source: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
