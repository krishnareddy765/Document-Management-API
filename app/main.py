from fastapi import FastAPI
from app.routes.auth import router as auth_router, limiter
from app.routes.document import router as document_router
from app.database import Base, engine
from app.models.user import User
from app.models.document import Document
from app.models.document_status_history import DocumentStatusHistory

from app.core.exception_handler import app_exception_handler, generic_exception_handler
from app.core.exceptions import AppException

# 👇 RATE LIMIT IMPORTS
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📄 Document Management API",
    description="Upload ➜ Admin Approval ➜ Public Access",
    version="1.0.0",
    contact={
        "name": "Krishna",
        "email": "krishna@gmail.com"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# 👇 CONNECT LIMITER TO APP
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# 👇 GLOBAL RATE LIMIT EXCEPTION HANDLER
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "message": "Too many requests. Please try again later."
        }
    )


# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers
app.include_router(auth_router)
app.include_router(document_router)

# ROOT ROUTE
@app.get("/")
def root():
    return {"message": "Document Management API is Running 🚀"}