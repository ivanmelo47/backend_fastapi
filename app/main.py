from fastapi import FastAPI
from app.api.v1.api import router as api_router
from app.database import engine, Base

app = FastAPI(
    title="FastAPI MySQL CRUD",
    description="A complete CRUD example with FastAPI and MySQL",
    version="1.0.0"
)

# Crear tablas en la base de datos (solo para desarrollo)
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MySQL CRUD example"}