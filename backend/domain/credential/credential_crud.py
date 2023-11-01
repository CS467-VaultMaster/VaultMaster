from datetime import datetime
from starlette import status
from sqlalchemy.orm import Session
from domain.credential.credential_schema import (
    CredentialCreate,
    CredentialUpdate,
    CredentialResponse,
)
from models import (
    User,
    Vault,
    Credential,
)
import uuid
from fastapi import HTTPException
from domain.vault.vault_crud import get_vault_by_user_id


def create_credential(db: Session, user: User, credential_create: CredentialCreate) -> Credential:
    user_vault = get_vault_by_user_id(db, user.id)
    db_credential = Credential(
        id=str(uuid.uuid4()),
        nickname=credential_create.nickname,
        category=credential_create.category,
        url=credential_create.url,
        password=credential_create.password,
        note=credential_create.note,
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        vault=user_vault,
    )
    db.add(db_credential)
    db.commit()
    return get_credential_by_id(db, db_credential.id)



def get_credentials(db: Session, user: User):
    user_vault = get_vault_by_user_id(db, user.id)

    return db.query(Credential).filter(Credential.vault_id == user_vault.id).all()


def get_credential_by_id(db: Session, credential_id: str) -> Credential | None:
    return db.query(Credential).filter(Credential.id == credential_id).first()