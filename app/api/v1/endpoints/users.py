from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserOut
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.database import get_db
from app.services.responses import response_success, response_error

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.create_user(user)

@router.get("/", response_model=list[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.get_users(skip, limit)

""" @router.get("/test-error")
def test_error():
    return response_error(mensaje="No se pudo procesar tu solicitud", codigo=422) """

@router.get("/uuid/{uuid}")
def read_user(uuid: str, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        user = user_service.get_user_by_uuid(uuid)
        return response_success(
            data=UserOut.model_validate(user),
            mensaje="Usuario obtenido correctamente"
        )
    except HTTPException as e:
        return response_error(mensaje=e.detail, codigo=e.status_code)

@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.get_user(user_id)

@router.put("/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    user_service.delete_user(user_id)
    return None