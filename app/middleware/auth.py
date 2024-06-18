from functools import wraps
import jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.settings import JWT_SECRET_KEY, JWT_ALGORITHM
from app.database import get_db
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import HTTPException, status, Depends, Security
from app.models import User
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid tokennnn")
    
def auth_required(func):
    @wraps(func)
    def wrapper(current_user: User = Depends(get_current_user), *args, **kwargs):
        return func(current_user, *args, **kwargs)
    return wrapper

