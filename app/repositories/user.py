# app/repositories/user.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime  # Añade esto al inicio del archivo
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_uuid(self, uuid: str):
        return self.db.query(User).filter(User.uuid == uuid).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_users_filtered(self, skip: int = 0, limit: int = 100, exclude_roles: list[str] = [], only_active: bool = False):
        query = self.db.query(User)
        
        if exclude_roles:
            query = query.filter(User.rol.notin_(exclude_roles))

        if only_active:
            query = query.filter(User.status == 1)

        return query.offset(skip).limit(limit).all()


    def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            created_at=datetime.now(settings.tz),
            updated_at=datetime.now(settings.tz)
        )

        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "codigo": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "mensaje": ["Error al crear el usuario", str(e)],
                    "data": None
                }
            )

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = user.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = pwd_context.hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            del update_data["password"]

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "codigo": 500,
                    "mensaje": ["Error al actualizar el usuario", str(e)],
                    "data": None
                }
            )


    def delete_user(self, user_id: int):
        db_user = self.get_user(user_id)
        if not db_user:
            return False

        try:
            self.db.delete(db_user)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "codigo": 500,
                    "mensaje": ["Error al eliminar el usuario", str(e)],
                    "data": None
                }
            )