from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from jose import jwt
from app.settings import JWT_SECRET_KEY, JWT_ALGORITHM
from app.middleware.auth import auth_required, get_current_user
from app.utils import authenticate_user,create_access_token
from pydantic import BaseModel, EmailStr

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
@router.post("/login")
async def login(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password  
    user = await authenticate_user(email, password)
    if not user:
        logger.error("user missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"email": user.email}
    )

    return access_token

@router.post("/register")
async def register(data: LoginRequest,db: Session = Depends(get_db)):
    try:
        email = data.email
        password = data.password  
        hashed_password = User.hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        access_token = create_access_token(
            data={"email": user.email}
        )
        return access_token
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        logger.debug("Payload decoded: %s", payload)
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        new_tokens = create_access_token(data={"email": email})
        return new_tokens
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.get("/token-test")
@auth_required
def token_test_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": "Token is valid", "user": current_user}