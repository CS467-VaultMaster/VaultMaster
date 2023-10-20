from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from database import get_db
from domain.user.user_crud import (
    pwd_context,
    create_user,
    update_user,
    remove_user,
    get_existing_user,
    get_user_by_username,
    get_user_by_id,
)
from domain.user.user_schema import UserCreate, UserUpdate, UserResponse, Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User

router = APIRouter(prefix="/vaultmaster/user")

ACCESS_TOKEN_EXPIRE_MINUTES = 10
SECRET_KEY = "SECRET"
ALGORITHM = "HS512"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/vaultmaster/user/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Authenticates the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception
        return user


@router.post("/register", response_model=UserResponse)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """
    User registration endpoint.
    """
    user = get_existing_user(db, user_create=user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already exists.",
        )
    return create_user(db=db, user_create=user_create)


@router.get("/account")
def user_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> UserResponse:
    """
    Returns the user information.
    """
    return get_user_by_id(db=db, id=current_user.id)


@router.put("/account")
def user_update(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> UserResponse:
    """
    User profile update endpoint.
    """
    return update_user(db=db, user_update=user_update, current_user=current_user)


@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
def user_remove(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    This endpoint removes the user self from the database.
    """
    remove_user(db, current_user)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login endpoint that returns a token.
    """
    user = get_user_by_username(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id,
    }
