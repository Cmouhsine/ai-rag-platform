import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.models.document import Document
from app.rag.loader import PDFLoader
from app.repositories.document_repository import DocumentRepository
from app.rag.chunker import TextChunker
from app.rag.embeddings import EmbeddingService

UPLOAD_DIRECTORY = Path("data/uploads")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository
        self.loader = PDFLoader()
        self.chunker = TextChunker()
        self.embedding_service = EmbeddingService()

    def upload_document(
        self,
        file: UploadFile,
        owner_id: int,
    ):

        extension = Path(
            file.filename
        ).suffix

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        destination = (
            UPLOAD_DIRECTORY / unique_filename
        )

        with destination.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            content_type=file.content_type,
            path=str(destination),
            owner_id=owner_id,
            status="UPLOADED",
        )

        document = self.repository.create(document)

        extracted_text = self.loader.load(document.path)

        chunks = self.chunker.split(extracted_text)
        
        embeddings = self.embedding_service.embed_documents(
            chunks
        )
        
        print("=" * 80)
        print(f"Document : {document.original_filename}")
        print(f"Characters : {len(extracted_text)}")
        print(f"Chunks : {len(chunks)}")
        print(f"Embeddings : {len(embeddings)}")
        print(f"Embedding dimension : {len(embeddings[0])}")
        print("=" * 80)
        
        return document
    
