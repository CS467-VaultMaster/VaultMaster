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
import subprocess
from cryptography.fernet import Fernet


def create_credential(
    db: Session, user: User, credential_create: CredentialCreate
) -> Credential:
    user_vault = get_vault_by_user_id(db, user.id)
    fernet_key, cred_password = double_encrypt(user.id, credential_create.password)
    db_credential = Credential(
        id=str(uuid.uuid4()),
        nickname=credential_create.nickname,
        category=credential_create.category,
        url=credential_create.url,
        password=cred_password,
        note=credential_create.note,
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        fernet_key=fernet_key,
        vault=user_vault,
    )
    db.add(db_credential)
    db.commit()
    return get_credential_by_id(db, db_credential.id)


def update_credential(
    db: Session,
    credential_id: str,
    credential_update: CredentialUpdate,
    current_user: User,
) -> Credential:
    credential = get_credential_by_id(db, credential_id)
    # TODO: Check if the user has access to this credential.
    credential.nickname = (credential_update.nickname,)
    credential.category = (credential_update.category,)
    credential.url = (credential_update.url,)
    credential.password = (credential_update.password,)
    credential.note = (credential_update.note,)
    credential.modified = datetime.utcnow()
    db.add(credential)
    db.commit()
    return get_credential_by_id(db, credential_id)


def remove_credential(db: Session, credential_id: str, current_user: User):
    credential = get_credential_by_id(db, credential_id)
    db.delete(credential)
    db.commit()


def get_credentials(db: Session, user: User):
    user_vault = get_vault_by_user_id(db, user.id)

    return db.query(Credential).filter(Credential.vault_id == user_vault.id).all()


def get_credential_by_id(db: Session, credential_id: str) -> Credential | None:
    return db.query(Credential).filter(Credential.id == credential_id).first()


def double_encrypt(user_id: str, cred_password: str) -> list[str]:
    fernet_key = Fernet.generate_key()
    f = Fernet(fernet_key)
    encrypted_password = f.encrypt(cred_password.encode())

    fernet_key_decoded = fernet_key.decode()
    encrypted_password_decoded = encrypted_password.decode()

    cipher_fernet_key = cipher_encrypt(user_id, fernet_key_decoded)
    cipher_cred_password = cipher_encrypt(user_id, encrypted_password_decoded)

    return [cipher_fernet_key, cipher_cred_password]


def double_decrypt(user_id: str, cred_password: str) -> list[str]:
    pass


def cipher_encrypt(password: str, data: str) -> str:
    encrypted_str = subprocess.check_output(
        ["./cipher_cmd", "enc", f"{password}", f"{data}"]
    )
    return encrypted_str


def cipher_decrypt(password: str, data: str) -> str:
    decrypted_str = subprocess.check_output(
        ["./cipher_cmd", "dec", f"{password}", f"{data}"]
    )
    return decrypted_str
