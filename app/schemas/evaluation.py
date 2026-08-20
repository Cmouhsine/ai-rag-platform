from pydantic import BaseModel


class EvaluationRequest(BaseModel):

    question: str

    expected_answer: str

    expected_keywords: list[str] = []

    top_k: int = 5


class EvaluationResponse(BaseModel):

    question: str

    expected_answer: str

    generated_answer: str

    retrieved_chunks: int

    keyword_score: float

    retrieval_score: float

    overall_score: float