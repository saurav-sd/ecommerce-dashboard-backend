from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.user import UserCreate, UserOut, RefreshTokenSchema
from app.db.models.user import User
from app.crud.user import get_user_by_email, create_user
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, create_and_store_refresh_token, verify_password, require_role
from app.db.models.refresh_token import RefreshToken
from datetime import timedelta
from app.core.config import settings
from datetime import datetime
import secrets


router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if the user already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create the new user
    new_user = create_user(db, user)
    return new_user


@router.post("/login")
def login_user(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, from_data.username)
    print("User : ", user.__dict__)
    if not user or not verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(user.id, role=user.role.value, expires_delta=access_token_expires)

    # Create and store refresh token (this commits to DB)
    refresh_token = create_and_store_refresh_token(db=db, user_id=user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "token_type": "bearer"
    }


@router.post("/refresh-token")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter_by(token=refresh_token).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if db_token.revoked or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired or revoked")

    user = db.query(User).filter_by(id=db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(user_id=user.id,role=user.role.value,expires_delta=timedelta(minutes=15))
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout_user(payload: RefreshTokenSchema, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter_by(token=payload.refresh_token).first()
    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found")

    db_token.revoked = True
    db.commit()
    return {"msg": "Logged out successfully"}

@router.get("/admin/dashboard")
def get_admin_dashboard(current_user=Depends(require_role(["admin"]))):
    return {"msg": "Welcome to the admin dashboard"}

@router.get("/seller/products")
def get_seller_products(current_user=Depends(require_role(["seller", "admin"]))):
    return {"msg": "Products list for seller or admin"}
