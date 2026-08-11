from pydantic import BaseModel


class RAGRequest(BaseModel):
    question: str
    top_k: int = 5


class RAGSource(BaseModel):
    document_id: int
    chunk_index: int
    distance: float


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]