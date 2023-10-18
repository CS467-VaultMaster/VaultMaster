from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate, UserUpdate, UserResponse
from models import User
from passlib.context import CryptContext
import uuid
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate) -> None:
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

def get_existing_user(db: Session, user_create: UserCreate) -> User | None:
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()