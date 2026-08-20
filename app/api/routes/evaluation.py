from fastapi import APIRouter

from app.rag.evaluator import RAGEvaluator
from app.schemas.evaluation import (
    EvaluationRequest,
    EvaluationResponse,
)


router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


@router.post(
    "/rag",
    response_model=EvaluationResponse,
)
def evaluate_rag(
    request: EvaluationRequest,
):

    evaluator = RAGEvaluator()

    result = evaluator.evaluate_case(
        question=request.question,
        expected_answer=request.expected_answer,
        expected_keywords=request.expected_keywords,
        top_k=request.top_k,
    )

    return result