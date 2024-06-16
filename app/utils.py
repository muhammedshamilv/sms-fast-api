from .models import User 
from sqlalchemy.orm import Session
from .database import SessionLocal
from .settings import JWT_SECRET_KEY, JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS
from jose import jwt


from datetime import datetime, timedelta
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def get_user(email: str, db: Session = SessionLocal()) -> User:
    return db.query(User).filter(User.email == email).first()

async def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return None
    if not User.verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict):
    to_encode = data.copy()

    access_token_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": access_token_expire})
    access_token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    refresh_token_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": refresh_token_expire})
    refresh_token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }