from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from jose import jwt
from app.settings import JWT_SECRET_KEY, JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS

from app.utils import authenticate_user,create_access_token
router = APIRouter()

@router.post("/login")
async def login(email,password):    
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return access_token

@router.post("/register")
async def register(email,password,db: Session = Depends(get_db)):
    try:
        hashed_password = User.hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return access_token
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        new_tokens = create_access_token(data={"sub": email})
        return new_tokens
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
