from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate, UserUpdate, UserResponse
from models import User
from passlib.context import CryptContext
import uuid
from datetime import datetime
from domain.vault.vault_crud import create_vault
from domain.vault.vault_schema import VaultCreate
import pyotp


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    #TODO: encode otp secret?
    otp = generate_otp()
    db_user = User(
        id=str(uuid.uuid4()),
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        last_verified=datetime.utcnow(),
        last_login_attempt=datetime.utcnow(),
        login_attempts=0,
        otp_secret=otp,
    )

    db.add(db_user)
    db.commit()
    user = get_user_by_username(db, user_create.username)
    # After creating a user, create a new vault and assign it to the new user.
    create_vault(db, user, VaultCreate(vault_name=f"{user.username}'s vault."))
    return get_user_by_username(db, user.username)


def update_user(
    db: Session, user_update: UserUpdate, current_user: User
) -> User | None:
    """
    Updates user information.
    """
    # TODO: Change to id?
    user = get_user_by_username(db, current_user.username)
    user.username = user_update.username
    user.password = pwd_context.hash(user_update.password1)
    user.email = user_update.email
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.modified = datetime.utcnow()
    db.add(user)
    db.commit()
    return get_user_by_username(db, user.username)


def update_login_attempts(
    db: Session,
    current_user: User,
    login_attempts: int = 0,
    last_login_attempt: datetime = None,
) -> None:
    """
    Update user's login attempts.
    """
    user = get_user_by_username(db, current_user.username)
    user.login_attempts += login_attempts
    if last_login_attempt:
        user.last_login_attempt = last_login_attempt
    db.add(user)
    db.commit()


def remove_user(db: Session, current_user: User) -> None:
    """
    Removes a user.
    """
    db.delete(current_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate) -> User | None:
    """
    Fetches user with the given username or email.
    """
    return (
        db.query(User)
        .filter(
            (User.username == user_create.username) | (User.email == user_create.email)
        )
        .first()
    )


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Fetches user with the given username
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, id: str) -> User | None:
    """
    Fetches user with the given id.
    """
    return db.query(User).filter(User.id == id).first()


def generate_otp() -> str:
    key = pyotp.random_base32()
    return key
