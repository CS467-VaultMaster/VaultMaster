from datetime import datetime

from sqlalchemy.orm import Session
from domain.vault.vault_schema import VaultCreate
from models import (
    User,
    Vault,
)
import uuid


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


def get_vaults(db: Session):
    """
    TODO: REMOVE THIS - TEST ONLY.
    """
    vaults = db.query(Vault).all()
    for vault in vaults:
        print(vault.user)
        print(vault.user_id)


def get_vault_by_user_id(db: Session, user_id: str) -> Vault | None:
    """
    Returns a vault that is assigned to the given user.
    """
    return db.query(Vault).filter(Vault.user_id == user_id).first()
