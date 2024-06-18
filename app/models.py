from sqlalchemy import Column, String,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from .database import Base
from datetime import datetime
from .settings import PSWD_SECRET_KEY
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    email = Column(String, unique=True)
    hashed_password = Column(String)

    @staticmethod
    def hash_password(password: str) -> str:
        password_with_secret = (password + PSWD_SECRET_KEY).encode()
        hashed_password = bcrypt.hashpw(password_with_secret, bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        plain_password_with_secret = (plain_password + PSWD_SECRET_KEY).encode()
        return bcrypt.checkpw(plain_password_with_secret, hashed_password.encode())
