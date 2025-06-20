from fastapi.exceptions import RequestValidationError
from fastapi import Request
from app.services.responses import response_error
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.exceptions.campos_alias import NOMBRE_CAMPOS

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    mensajes = []

    for error in exc.errors():
        loc = error.get("loc", [])
        campo_crudo = next((part for part in loc if part != "body"), None)
        campo = NOMBRE_CAMPOS.get(campo_crudo, campo_crudo)

        mensaje_raw = error.get("msg", "")

        if mensaje_raw == "Field required":
            mensaje = f"El campo {campo} es obligatorio"
        else:
            if ',' in mensaje_raw:
                mensaje = mensaje_raw.split(',', 1)[1].strip()
            else:
                mensaje = mensaje_raw

        mensajes.append(mensaje)

    return response_error(
        codigo=HTTP_422_UNPROCESSABLE_ENTITY,
        mensaje=mensajes,
        data=None
    )
