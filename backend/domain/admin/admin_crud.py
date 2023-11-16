from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from models import User, Admin
from datetime import datetime


def check_user_status(db: Session, user: User) -> bool:
    user_in_admin_db = (
        db.query(Admin)
        .filter(Admin.user_id == user.id and Admin.username == user.username)
        .first()
    )
    admin_num = len(db.query(Admin).all())
    if user_in_admin_db and user.is_admin and admin_num <= 3:
        return True
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="NOT FOUND",
        headers={"WWW-Authenticate": "Bearer"},
    )
