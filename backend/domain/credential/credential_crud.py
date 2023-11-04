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
        password=cred_password.decode(),
        note=credential_create.note,
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        fernet_key=fernet_key.decode(),
        vault=user_vault,
    )
    db.add(db_credential)
    db.commit()
    credential = get_credential_by_id(db, db_credential.id)
    return CredentialResponse(
        id=credential.id,
        nickname=credential.nickname,
        category=credential.category,
        url=credential.url,
        password=credential.password,
        note=credential.note,
        created=credential.created,
        modified=credential.modified,
    )


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


def get_credentials(db: Session, user: User) -> list[CredentialResponse]:
    user_vault = get_vault_by_user_id(db, user.id)
    return_lst = []
    credential_lst = (
        db.query(Credential).filter(Credential.vault_id == user_vault.id).all()
    )
    for credential in credential_lst:
        # Decrypt the password.
        decrypted_pwd = double_decrypt(user.id, credential)
        credential = CredentialResponse(
            id=credential.id,
            nickname=credential.nickname,
            category=credential.category,
            url=credential.url,
            password=decrypted_pwd,
            note=credential.note,
            created=credential.created,
            modified=credential.modified,
        )
        return_lst.append(credential)

    return return_lst


def get_credential_by_id(db: Session, credential_id: str) -> Credential | None:
    return db.query(Credential).filter(Credential.id == credential_id).first()


def double_encrypt(user_id: str, cred_password: str) -> list[str]:
    # First encryption.
    fernet_key = Fernet.generate_key()
    f = Fernet(fernet_key)
    encrypted_password = f.encrypt(cred_password.encode())

    fernet_key_decoded = fernet_key.decode()
    encrypted_password_decoded = encrypted_password.decode()
    # Second encryption.
    cipher_fernet_key = cipher_encrypt(user_id, fernet_key_decoded)
    cipher_cred_password = cipher_encrypt(user_id, encrypted_password_decoded)

    return [cipher_fernet_key, cipher_cred_password]


def double_decrypt(user_id: str, credential: Credential) -> StopAsyncIteration:
    db_fernet_key = credential.fernet_key
    db_password = credential.password
    # Un-doing the second encryption.
    deciphered_fernet_key = cipher_decrypt(user_id, db_fernet_key)
    deciphered_password = cipher_decrypt(user_id, db_password)
    # Un-doing the first encryption.
    f = Fernet(deciphered_fernet_key)
    decrypted_password = f.decrypt(deciphered_password)

    return decrypted_password.decode()


def cipher_encrypt(password: str, data: str) -> str:
    encrypted_str = subprocess.check_output(
        ["./cipher_cmd", "enc", f"{password}", f"{data}"]
    )
    return encrypted_str


def cipher_decrypt(password: str, data: str) -> str:
    try:
        decrypted_str = subprocess.check_output(
            ["./cipher_cmd", "dec", f"{password}", f"{data}"]
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output
            )
        )
    return decrypted_str


def get_creds_raw_format(db: Session, user: User):
    user_vault = get_vault_by_user_id(db, user.id)
    return db.query(Credential).filter(Credential.vault_id == user_vault.id).all()
