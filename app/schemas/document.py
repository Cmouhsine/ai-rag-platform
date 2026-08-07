from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):

    id: int

    filename: str

    original_filename: str

    content_type: str

    status: str

    owner_id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }