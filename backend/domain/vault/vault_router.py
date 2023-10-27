from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.vault.vault_schema import (
    VaultCreate,
    VaultUpdate,
    VaultResponse,
)
from domain.vault.vault_crud import (
    create_vault,
    get_vaults,
    get_vault_by_user_id,
)
from domain.user.user_crud import get_user_by_id
from domain.user.user_router import get_current_user
from models import (
    User,
    Vault,
)


router = APIRouter(prefix="/vaultmaster/vault")


@router.get("/all")
def get_all_vaults(db: Session = Depends(get_db)):
    """
    TODO: REMOVE THIS - TEST ENDPOINT.
    """
    get_vaults(db)


@router.get("/")
def get_user_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns current user's vault.
    """
    return get_vault_by_user_id(db, current_user.id)
