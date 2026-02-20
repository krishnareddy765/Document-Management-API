# app/models/document.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    uploaded_by = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")