# app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserOut
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.database import get_db
from app.services.responses import response_success, response_error
from app.core.security import admin_required
from app.core.security import verificar_acceso_usuario

router = APIRouter(prefix="/users", tags=["users"])

# Dependencia para inyectar el servicio de usuario sin repetir código
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    service = UserService(repo)
    return service

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        created_user = user_service.create_user(user)
        return response_success(
            data=UserOut.model_validate(created_user),
            mensaje=["Usuario creado correctamente"],
            codigo=status.HTTP_201_CREATED,
        )
    except HTTPException as e:
        return response_error(mensaje=e.detail, codigo=e.status_code)

@router.get("/", status_code=status.HTTP_200_OK)
def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    users = user_service.get_users(skip, limit)
    # Retornamos lista con el formato uniforme y modelos Pydantic
    return response_success(
        data=[UserOut.model_validate(user) for user in users],
        mensaje=["Usuarios obtenidos correctamente"],
        codigo=status.HTTP_200_OK,
    )

# Para evitar conflicto con /{user_id}, cambiamos prefijo para UUID
@router.get("/uuid/{uuid}", status_code=status.HTTP_200_OK)
def read_user_by_uuid(
    uuid: str,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.get_user_by_uuid(uuid)
        return response_success(
            data=UserOut.model_validate(user),
            mensaje=["Usuario obtenido correctamente"],
            codigo=status.HTTP_200_OK,
        )
    except HTTPException as e:
        return response_error(mensaje=e.detail, codigo=e.status_code)

@router.get("/id/{user_id}", status_code=status.HTTP_200_OK)
def read_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.get_user(user_id)
        return response_success(
            data=UserOut.model_validate(user),
            mensaje=["Usuario obtenido correctamente"],
            codigo=status.HTTP_200_OK,
        )
    except HTTPException as e:
        return response_error(mensaje=e.detail, codigo=e.status_code)

@router.put("/id/{user_id}", status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user=Depends(verificar_acceso_usuario),  # ✅ Pasas solo la función
):
    try:
        updated_user = user_service.update_user(user_id, user_update)
        return response_success(
            data=UserOut.model_validate(updated_user),
            mensaje=["Usuario actualizado correctamente"],
            codigo=status.HTTP_200_OK,
        )
    except HTTPException as e:
        raise e
        #return response_error(mensaje=e.detail, codigo=e.status_code)
    

@router.delete("/id/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_service.delete_user(user_id)
        return response_success(
            data=None,
            mensaje=["Usuario eliminado correctamente"],
            codigo=status.HTTP_200_OK,
        )
    except HTTPException as e:
        raise e
        #return response_error(mensaje=e.detail, codigo=e.status_code)