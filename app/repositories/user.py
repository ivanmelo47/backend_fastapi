# app/repositories/user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime  # Añade esto al inicio del archivo

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

    def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),  # Establece manualmente las fechas
            updated_at=datetime.utcnow()   # para asegurar que no sean None
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

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
            
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user(user_id)
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True