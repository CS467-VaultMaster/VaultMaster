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
    update_login_attempts,
)
from domain.user.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    Token,
    UserResponseRegistration,
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User
import pyotp

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


@router.post("/register", response_model=UserResponseRegistration)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponseRegistration:
    """
    User registration endpoint.
    Returns the new user info.
    """
    user = get_existing_user(db, user_create=user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already exists.",
        )
    new_user = create_user(db=db, user_create=user_create)

    otp_uri = pyotp.totp.TOTP(new_user.otp_secret).provisioning_uri("VaultMaster")

    return UserResponseRegistration(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        created=new_user.created,
        modified=new_user.modified,
        last_login_attempt=new_user.last_login_attempt,
        login_attempts=new_user.login_attempts,
        otp_uri=otp_uri,
    )


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
    Returns the user info with updated data.
    """
    return update_user(db=db, user_update=user_update, current_user=current_user)


@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
def user_remove(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    This endpoint removes the user self from the database.
    The user's vault is also removed from this endpoint.
    """
    remove_user(db, current_user)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login endpoint that returns a token.
    """
    # TODO: Clean up and refactor.
    user = get_user_by_username(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        # If user exists but did not enter the correct credential.
        if user:
            # Check how many login attempts the user has made.
            check_login_attempts(db, user)
            # Add one to the login attempts.
            update_login_attempts(db, user, 1, user.last_login_attempt)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Catch the situation where the user enters in the correct credential while wating.
    check_login_attempts(db, user)
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    update_login_attempts(db, user, -(user.login_attempts), datetime.utcnow())
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id,
    }


@router.get("/otp_verify/{code}", status_code=200)
def otp_verify(code: str, user: User = Depends(get_current_user)) -> bool:
    otp_key = user.otp_secret
    value_to_verity = pyotp.TOTP(otp_key)
    if value_to_verity.verify(code):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect OTP code.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_login_attempts(db: Session, current_user: User):
    # If the user has more than 3 login attempts.
    if current_user.login_attempts == 3:
        # If 10 minutes have not passed.
        if datetime.utcnow() < current_user.last_login_attempt:
            remainder = (
                current_user.last_login_attempt - datetime.utcnow()
            ).total_seconds()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Too many failed login attempts. Please try again in {remainder} seconds.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            # 10 minutes have passed.  Bring the user's login_attempts count down to 0.
            update_login_attempts(db, current_user, -(current_user.login_attempts))
    # If the user got to the third unsucessful attempt.
    if current_user.login_attempts == 2:
        # Add 10 minutes to last_login_attempt.
        new_time = current_user.last_login_attempt + timedelta(minutes=10)
        update_login_attempts(db, current_user, 0, new_time)
