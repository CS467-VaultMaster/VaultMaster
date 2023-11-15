from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime
from database import get_db

from domain.user.user_router import get_current_user
from models import Admin, User


router = APIRouter(prefix="/vaultmaster/admin")


@router.get("/admin_list")
def get_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Admin).all()


@router.get("/user_account/{user_id}")
def user_account_get_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.put("/user_account/{user_id}")
def user_account_update_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.delete("/user_account/{user_id}")
def user_account_delete_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.get("/user_vault/{user_id}")
def user_vault_get_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.put("/user_vault/{user_id}")
def user_vault_update_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass
