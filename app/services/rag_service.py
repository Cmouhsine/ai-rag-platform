from app.rag.llm import LLMService
from app.rag.retriever import Retriever


class RAGService:

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ):

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        context = "\n\n".join(
            result["content"]
            for result in results
        )

        answer = self.llm.generate(
            question=question,
            context=context,
        )

        return {
            "answer": answer,
            "sources": [
                {
                    "document_id": result["metadata"]["document_id"],
                    "chunk_index": result["metadata"]["chunk_index"],
                    "distance": result["distance"],
                }
                for result in results
            ],
        }