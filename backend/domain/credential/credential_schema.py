from pydantic import BaseModel, validator
from datetime import datetime


class CredentialCreate(BaseModel):
    nickname: str | None = None
    category: str | None = None
    url: str
    password: str
    note: str | None = None

    @validator("url", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("This is a required field.")
        return v


class CredentialUpdate(BaseModel):
    nickname: str | None = None
    category: str | None = None
    url: str
    password: str
    note: str | None = None

    @validator("url", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("This is a required field.")
        return v


class CredentialResponse(BaseModel):
    id: str
    nickname: str
    category: str
    url: str
    password: str
    note: str
    created: datetime
    modified: datetime
    #vault_id: str