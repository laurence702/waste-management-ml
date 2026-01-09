from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="EcoOps API", version="0.1.0", lifespan=lifespan)
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to EcoOps Waste Management API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
