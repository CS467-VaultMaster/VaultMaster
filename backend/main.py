import os
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ["POSTGRES_PASSWORD"] + "@database:5432/vaultmaster"

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
