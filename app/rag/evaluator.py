from dataclasses import dataclass
from typing import Any

from app.rag.retriever import Retriever
from app.rag.llm import LLMService


@dataclass
class EvaluationResult:

    question: str

    expected_answer: str

    generated_answer: str

    retrieved_chunks: int

    keyword_score: float

    retrieval_score: float

    overall_score: float


class RAGEvaluator:

    def __init__(self):

        self.retriever = Retriever()

        self.llm = LLMService()

    def evaluate_case(
        self,
        question: str,
        expected_answer: str,
        expected_keywords: list[str],
        top_k: int = 5,
    ) -> EvaluationResult:

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        context = "\n\n".join(
            result["content"]
            for result in results
        )

        generated_answer = self.llm.generate(
            question=question,
            context=context,
        )

        keyword_score = self._keyword_score(
            generated_answer,
            expected_keywords,
        )

        retrieval_score = self._retrieval_score(
            results,
        )

        overall_score = (
            keyword_score * 0.6
            + retrieval_score * 0.4
        )

        return EvaluationResult(
            question=question,
            expected_answer=expected_answer,
            generated_answer=generated_answer,
            retrieved_chunks=len(results),
            keyword_score=keyword_score,
            retrieval_score=retrieval_score,
            overall_score=overall_score,
        )

    def _keyword_score(
        self,
        answer: str,
        keywords: list[str],
    ) -> float:

        if not keywords:
            return 0.0

        answer_lower = answer.lower()

        matched = sum(
            1
            for keyword in keywords
            if keyword.lower() in answer_lower
        )

        return matched / len(keywords)

    def _retrieval_score(
        self,
        results: list[dict[str, Any]],
    ) -> float:

        if not results:
            return 0.0

        distances = [
            result["distance"]
            for result in results
            if result.get("distance") is not None
        ]

        if not distances:
            return 0.0

        average_distance = (
            sum(distances) / len(distances)
        )

        score = 1.0 / (1.0 + average_distance)

        return min(score, 1.0)