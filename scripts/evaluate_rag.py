import json
from pathlib import Path

from app.rag.evaluator import RAGEvaluator


DATASET_PATH = Path(
    "data/evaluation/rag_dataset.json"
)


def main():

    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        dataset = json.load(file)

    evaluator = RAGEvaluator()

    results = []

    for case in dataset:

        result = evaluator.evaluate_case(
            question=case["question"],
            expected_answer=case["expected_answer"],
            expected_keywords=case.get(
                "expected_keywords",
                [],
            ),
            top_k=5,
        )

        results.append(
            {
                "question": result.question,
                "generated_answer": result.generated_answer,
                "keyword_score": result.keyword_score,
                "retrieval_score": result.retrieval_score,
                "overall_score": result.overall_score,
                "retrieved_chunks": result.retrieved_chunks,
            }
        )

        print("\n" + "=" * 80)

        print(
            f"Question: {result.question}"
        )

        print(
            f"Keyword score: "
            f"{result.keyword_score:.2f}"
        )

        print(
            f"Retrieval score: "
            f"{result.retrieval_score:.2f}"
        )

        print(
            f"Overall score: "
            f"{result.overall_score:.2f}"
        )

        print(
            f"Answer: "
            f"{result.generated_answer}"
        )

    output_path = Path(
        "data/evaluation/results.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nResults saved to {output_path}"
    )


if __name__ == "__main__":
    main()