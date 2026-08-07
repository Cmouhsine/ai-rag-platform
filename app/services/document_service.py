import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository

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

        return self.repository.create(document)