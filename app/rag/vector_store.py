import chromadb


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(
        self,
        document_id: int,
        chunks: list[str],
        embeddings: list[list[float]],
    ):

        ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def count(self) -> int:
        return self.collection.count()