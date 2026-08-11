from fastapi import APIRouter

from app.schemas.rag import RAGRequest
from app.schemas.rag import RAGResponse
from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/ask",
    response_model=RAGResponse,
)
def ask_question(
    request: RAGRequest,
):

    service = RAGService()

    return service.answer(
        question=request.question,
        top_k=request.top_k,
    )