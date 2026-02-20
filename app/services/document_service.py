# app/services/document_service.py

import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.document import Document


UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_document(file: UploadFile, db: Session, user_id: int):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    document = Document(
        filename=file.filename,
        file_path=file_path,
        uploaded_by=user_id,
        status="pending"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def approve_document(db: Session, document_id: int):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return None

    doc.status = "approved"
    db.commit()
    return doc


def get_user_documents(db: Session, user_id: int):
    return db.query(Document).filter(Document.uploaded_by == user_id).all()


def get_all_documents(db: Session):
    return db.query(Document).all()