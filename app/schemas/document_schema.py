# app/schemas/document_schema.py

from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True