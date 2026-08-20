from typing import Optional
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
 
class Retriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id: Optional[int] = None,
    ) -> list[dict]:

        query_embedding = (
            self.embedding_service
            .embed_documents([query])[0]
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {
                "content": content,
                "metadata": metadata,
                "distance": distance,
            }
            for content, metadata, distance
            in zip(documents, metadatas, distances)
        ]

