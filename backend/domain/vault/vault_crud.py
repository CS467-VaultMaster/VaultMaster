from datetime import datetime
from starlette import status
from sqlalchemy.orm import Session
from domain.vault.vault_schema import (
    VaultCreate,
    VaultUpdate,
    VaultOpen,
)
from models import (
    User,
    Vault,
)
import uuid
from fastapi import HTTPException


def create_vault(db: Session, user: User, vault_create: VaultCreate):
    db_vault = Vault(
        id=str(uuid.uuid4()),
        vault_name=vault_create.vault_name,
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        open_attempts=0,
        user=user,
    )
    db.add(db_vault)
    db.commit()


def get_vault_by_user_id(db: Session, user_id: str) -> Vault | None:
    """
    Returns a vault that is assigned to the given user.
    """
    return db.query(Vault).filter(Vault.user_id == user_id).first()


def update_vault(db: Session, vault_update: VaultUpdate, current_user: User) -> Vault:
    """
    Updates user vault.
    """
    user_vault = db.query(Vault).filter(Vault.user_id == current_user.id).first()
    user_vault.vault_name = vault_update.vault_name
    user_vault.modified = datetime.utcnow()
    db.add(user_vault)
    db.commit()
    return db.query(Vault).filter(Vault.user_id == current_user.id).first()


def open_vault(vault_open: VaultOpen, current_user: User) -> bool:
    """
    Compares user input to user's password and opens the vault if verified.
    """
    from domain.user.user_crud import pwd_context
    if not pwd_context.verify(vault_open.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )
    return True
