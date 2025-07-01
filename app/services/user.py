# app/services/user.py

from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserInDB

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        db_user = self.user_repository.get_user(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "codigo": status.HTTP_404_NOT_FOUND,
                    "mensaje": ["Usuario no encontrado"],
                    "data": None
                }
            )
        return db_user
    
    def get_user_by_uuid(self, uuid: str):
        db_user = self.user_repository.get_user_by_uuid(uuid)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return db_user

    def get_user_by_email(self, email: str):
        db_user = self.user_repository.get_user_by_email(email)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

    def get_users(self, skip: int = 0, limit: int = 100, current_user=None):
        # Si es admin, solo puede ver usuarios con rol 'user'
        if current_user.rol == "admin":
            return self.user_repository.get_users_filtered(
                skip=skip,
                limit=limit,
                exclude_roles=["admin"]
            )
        return self.user_repository.get_users(skip, limit)
    
    def create_user(self, user: UserCreate):
        errores = []

        if self.user_repository.get_user_by_email(user.email):
            errores.append("Este email ya está registrado")
        
        if self.user_repository.get_user_by_username(user.username):
            errores.append("Este username ya está registrado")

        if errores:
            # Lanza una sola excepción con todos los errores juntos
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errores
            )

        return self.user_repository.create_user(user)

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.get_user(user_id)  # ✅ Usa validación centralizada
        
        # ⛔ Validar si el usuario está inactivo (status = 0)
        if db_user.status == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "codigo": status.HTTP_403_FORBIDDEN,
                    "mensaje": ["No se puede editar un usuario que no está activo"],
                    "data": None
                }
            )

        errores = []

        if user.username is not None:
            existing_user = self.user_repository.get_user_by_username(user.username)
            if existing_user and existing_user.id != user_id:
                errores.append("Este username ya está registrado")

        if user.email is not None:
            existing_user = self.user_repository.get_user_by_email(user.email)
            if existing_user and existing_user.id != user_id:
                errores.append("Este email ya está registrado")

        if errores:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "codigo": status.HTTP_403_FORBIDDEN,
                    "mensaje": errores,
                    "data": None
                }
            )

        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: int):
        self.get_user(user_id)  # ✅ Solo llama, si no existe, lanzará la excepción ya
        return self.user_repository.delete_user(user_id)