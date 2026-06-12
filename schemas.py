from pydantic import BaseModel
from datetime import datetime


# Response shape for document upload and list
class DocumentResponse(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy model


# Response shape for delete
class DeleteResponse(BaseModel):
    message: str
