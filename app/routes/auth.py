from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import create_user, authenticate_user
from app.utils.jwt_handler import create_access_token

# 👇 RATE LIMIT IMPORTS
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/auth", tags=["Auth"])

# 👇 CREATE LIMITER INSTANCE
limiter = Limiter(key_func=get_remote_address)


# 🔐 REGISTER API (5 requests per minute)
@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    create_user(db, user.email, user.password)
    return {
        "status": "success",
        "message": "User registered successfully"
    }


# 🔐 LOGIN API (5 requests per minute)
@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):

    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }