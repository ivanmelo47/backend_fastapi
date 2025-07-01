from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.api.v1.api import router as api_router
from app.database import engine, Base
from app.services.responses import response_error
from app.exceptions.handlers import validation_exception_handler

from fastapi.responses import JSONResponse

app = FastAPI(
    title="FastAPI MySQL CRUD",
    description="A complete CRUD example with FastAPI and MySQL",
    version="1.0.0"
)

# Registrar el manejador
# app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 👇 Este manejador intercepta TODAS las HTTPException (incluyendo CustomHTTPException)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Si el error ya tiene el formato personalizado (como CustomHTTPException)
    if isinstance(exc.detail, dict) and "codigo" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,  # 👈 Devuelve el contenido directamente sin "detail"
        )
    # Para otras HTTPException no personalizadas (poco probable en tu caso)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "codigo": exc.status_code,
            "mensaje": [str(exc.detail)],
            "data": None,
        },
    )

# Crear tablas en la base de datos (solo para desarrollo)
# Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MySQL CRUD example"}