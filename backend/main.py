from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.user import user_router
from domain.vault import vault_router
from domain.credential import credential_router
from domain.admin import admin_router

ORIGINS = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, tags=["User"])
app.include_router(vault_router.router, tags=["Vault"])
app.include_router(credential_router.router, tags=["Credential"])
app.include_router(admin_router.router, tags=["Admin"])
