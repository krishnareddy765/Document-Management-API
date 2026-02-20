# app/main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.models.document import Document
from app.routes.auth import router as auth_router
from app.routes.document import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Document Management API")

app.include_router(auth_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {"message": "API is running"}