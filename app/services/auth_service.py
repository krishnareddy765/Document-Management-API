from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_user(db: Session, email: str, password: str):

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("User already exists")

    # 🔥 CHECK IF FIRST USER
    user_count = db.query(User).count()

    if user_count == 0:
        role = "admin"
    else:
        role = "user"

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user