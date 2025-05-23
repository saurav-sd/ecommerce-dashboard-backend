from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from app.db.models.refresh_token import RefreshToken
from sqlalchemy.orm import Session
import secrets
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from app.db.models.user import User
from app.db.session import get_db



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    role: str,
    expires_delta: Optional[timedelta] = timedelta(minutes=15),
):
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_and_store_refresh_token(user_id: int, db: Session) -> str:
    refresh_token = secrets.token_urlsafe(64)
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    if not expires_at:
        raise Exception("expires_at is None!")

    db_token = RefreshToken(
        user_id=user_id,
        token=refresh_token,
        expires_at=expires_at,
        revoked=False
    )

    print("STORING REFRESH TOKEN:", db_token)

    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return refresh_token

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        return {"user_id": int(user_id), "role": role}
    except JWTError:
        raise credentials_exception

def require_role(required_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {current_user['role']}"
            )
        return current_user
    return role_checker

def get_current_active_user(
    current_user_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.id == current_user_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user