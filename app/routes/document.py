from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth_dependency import get_current_user, admin_only
from app.services.document_service import (
    save_document,
    approve_document,
    get_user_documents,
    get_all_documents
)
from app.schemas.document_schema import DocumentResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return save_document(file, db, current_user.id)


@router.get("/my-documents", response_model=list[DocumentResponse])
def my_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_documents(db, current_user.id)


# ✅ ADVANCED ADMIN QUERY
@router.get("/all")
def all_documents(
    status: str = Query(None),
    search: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50),
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return get_all_documents(
        db,
        status=status,
        search=search,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )


@router.put("/approve/{document_id}", response_model=DocumentResponse)
def approve(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    doc = approve_document(db, document_id, admin.id, background_tasks)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc