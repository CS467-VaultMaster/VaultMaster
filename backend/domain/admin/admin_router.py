from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime
from database import get_db
from domain.admin.admin_crud import check_user_status
from domain.user.user_router import get_current_user
from domain.user.user_crud import (
    get_user_by_id,
    get_all_users,
)
from models import Admin, User
from domain.user.user_schema import UserResponse


router = APIRouter(prefix="/vaultmaster/admin")


@router.get("/admin_list")
def admin_get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_user_status(db, current_user)
    return db.query(Admin).all()


@router.get("/user_account/all")
def user_account_get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_user_status(db, current_user)
    return get_all_users(db)


@router.get("/user_account/{user_id}")
def user_account_get_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    check_user_status(db, current_user)
    return get_user_by_id(db, user_id)


@router.put("/user_account/{user_id}")
def user_account_update_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.delete("/user_account/{user_id}")
def user_account_delete_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.get("/user_vault/{user_id}")
def user_vault_get_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.put("/user_vault/{user_id}")
def user_vault_update_admin(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.get("/user_credential/{user_id}/list")
def user_credential_get_admin_all(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.get("/user_credential/{user_id}/{credential_id}")
def user_credential_get_admin(
    user_id: str,
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.put("/user_credential/{user_id}/{credential_id}")
def user_credential_update_admin(
    user_id: str,
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass


@router.delete("/user_credential/{user_id}/{credential_id}")
def user_credential_delete_admin(
    user_id: str,
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass
