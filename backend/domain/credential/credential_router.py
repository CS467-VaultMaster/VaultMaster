from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.credential.credential_schema import (
    CredentialCreate,
    CredentialUpdate,
    CredentialResponse,
)
from domain.credential.credential_crud import (
    create_credential,
    get_credentials,
    update_credential,
    remove_credential,
)
from domain.user.user_router import get_current_user
from models import (
    User,
    Vault,
    Credential,
)

router = APIRouter(prefix="/vaultmaster/credential")


@router.get("/")
def get_user_credential(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_credentials(db, current_user)


@router.post("/", response_model=CredentialResponse)
def credential_create(
    credential_create: CredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Credential:
    return create_credential(db, current_user, credential_create)


@router.put("/{credential_id}")
def credential_update(
    credential_id: str,
    credential_update: CredentialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    update_credential(db, credential_id, credential_update, current_user)
    return get_credentials(db, current_user)


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
def credential_remove(
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_credential(db, credential_id, current_user)
