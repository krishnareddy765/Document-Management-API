import os
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import UploadFile, BackgroundTasks
from app.models.document import Document
from app.models.document_status_history import DocumentStatusHistory
from datetime import datetime

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def log_approval(document_id: int):
    print(f"Document {document_id} approved successfully")


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


def approve_document(db: Session, document_id: int, admin_id: int, background_tasks: BackgroundTasks):

    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return None

    doc.status = "approved"

    history = DocumentStatusHistory(
        document_id=document_id,
        status="approved",
        changed_by=admin_id
    )

    db.add(history)
    db.commit()

    background_tasks.add_task(log_approval, document_id)

    return doc


def get_user_documents(db: Session, user_id: int):
    return db.query(Document).filter(Document.uploaded_by == user_id).all()


# ✅ ADVANCED FILTERING
def get_all_documents(
        db: Session,
        status: str = None,
        search: str = None,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        page_size: int = 10
):

    query = db.query(Document)

    # Filter by status
    if status:
        query = query.filter(Document.status == status)

    # Search by filename
    if search:
        query = query.filter(Document.filename.ilike(f"%{search}%"))

    # Date filtering
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Document.uploaded_at >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(Document.uploaded_at <= end)

    # Pagination
    total = query.count()
    documents = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": documents
    }