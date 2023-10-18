from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from database import get_db
from domain.user.user_crud import pwd_context, create_user, get_existing_user
from domain.user.user_schema import UserCreate, UserUpdate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User

router = APIRouter(prefix="/vaultmaster/user")

"""
ACCESS_TOKEN_EXPIRE_MINUTES =
SECRET_KEY = 
ALGORITHM = 
"""


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register(user_create: UserCreate, db: Session = Depends(get_db)) -> None:
    user = get_existing_user(db, user_create=user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already exists.",
        )
    create_user(db=db, user_create=user_create)