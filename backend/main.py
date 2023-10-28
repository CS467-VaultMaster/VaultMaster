from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.user import user_router
from domain.vault import vault_router

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

app.include_router(user_router.router)
app.include_router(vault_router.router)

#############################
# TEST METHODS
# Please retain for testing (until we're ready to serve something else on the root path)
#############################

import os, psycopg2
from db_auth import get_db_auth

# Conceal secrets in .env file
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = get_db_auth()
# Allows interop between docker-compose and local dev
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_USER}"

@app.get("/")
def read_root():
	return {"message": "Hello from FastAPI"}

@app.get("/items/")
def read_items():
	with psycopg2.connect(DATABASE_URL) as conn:
		with conn.cursor() as curr:
			curr.execute("SELECT id, name FROM items")
			items = curr.fetchall()
			return [{"id": item[0], "name": item[1]} for item in items]