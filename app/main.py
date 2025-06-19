from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.api.v1.api import router as api_router
from app.database import engine, Base
from app.services.responses import response_error

app = FastAPI(
    title="FastAPI MySQL CRUD",
    description="A complete CRUD example with FastAPI and MySQL",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    mensajes = []
    for error in exc.errors():
        msg = error.get('msg', '')
        # Si el mensaje tiene coma, toma solo la parte después de la coma (tu mensaje personalizado)
        if ',' in msg:
            msg = msg.split(',', 1)[1].strip()
        mensajes.append(msg)

    return response_error(
        codigo=422,
        mensaje=mensajes,
        data=None
    )

# Crear tablas en la base de datos (solo para desarrollo)
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MySQL CRUD example"}