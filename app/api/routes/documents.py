from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.rag.retriever import Retriever

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),
):

    repository = DocumentRepository(db)

    service = DocumentService(repository)

    return service.upload_document(
        file=file,
        owner_id=1,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(

    db: Session = Depends(get_db),
):

    repository = DocumentRepository(db)

    return repository.list()

@router.get("/search")
def search_documents(
    query: str,
    top_k: int = 5,
):
    retriever = Retriever()

    return retriever.retrieve(
        query=query,
        top_k=top_k,
    )