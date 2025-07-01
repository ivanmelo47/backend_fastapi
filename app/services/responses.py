# app/services/responses.py

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional
from fastapi import HTTPException, status
from typing import Union


def response_success(
    data: Any,
    mensaje: str = "Operación exitosa",
    codigo: int = 200
) -> JSONResponse:
    return JSONResponse(
        status_code=codigo,
        content={
            "codigo": codigo,
            "mensaje": mensaje,
            "data": jsonable_encoder(data)
        }
    )


def response_error(
    mensaje: str = "Ocurrió un error",
    codigo: int = 400,
    data: Optional[Any] = None
) -> JSONResponse:
    return JSONResponse(
        status_code=codigo,
        content={
            "codigo": codigo,
            "mensaje": mensaje,
            "data": jsonable_encoder(data) if data else None
        }
    )
    
class CustomHTTPException(HTTPException):
    def __init__(
        self,
        mensaje: Union[str, list[str]],
        codigo: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None,
    ):
        if isinstance(mensaje, str):
            mensaje = [mensaje]
        super().__init__(
            status_code=codigo,
            detail={
                "codigo": codigo,  # 👈 Añadimos el código aquí
                "mensaje": mensaje,
                "data": data,
            },
        )
