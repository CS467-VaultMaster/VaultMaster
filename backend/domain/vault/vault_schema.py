from pydantic import BaseModel, validator
from datetime import datetime


class VaultCreate(BaseModel):
    vault_name: str

    @validator("vault_name")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Vault name cannot be empty.")
        return v


class VaultUpdate(BaseModel):
    vault_name: str

    @validator("vault_name")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Vault name cannot be empty.")
        return v


class VaultOpen(BaseModel):
    password: str

    @validator("password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Vault password cannot be empty.")
        return v


class VaultResponse(BaseModel):
    id: str
    vault_name: str
    created: datetime
    modified: datetime
    open_attempts: int
