from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate, UserUpdate, UserResponse
from models import User
from passlib.context import CryptContext
import uuid
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    db_user = User(
        id=str(uuid.uuid4()),
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        email=user_create.email,
        phone_number=user_create.phone_number,
        created=datetime.now(),
        modified=datetime.now(),
        last_verified=datetime.now(),
        login_attemtps=0,
    )
    db.add(db_user)
    db.commit()
    return get_user_by_username(db, user_create.username)


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
    user.phone_number = user_update.phone_number
    user.modified = datetime.now()
    db.add(user)
    db.commit()
    return get_user_by_username(db, user.username)


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