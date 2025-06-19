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
                detail="User not found"
            )
        return db_user
    
    def get_user_by_uuid(self, uuid: str):
        db_user = self.user_repository.get_user_by_uuid(uuid)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
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

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.user_repository.get_users(skip, limit)

    def create_user(self, user: UserCreate):
        db_user = self.user_repository.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        db_user = self.user_repository.get_user_by_username(user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
            
        return self.user_repository.create_user(user)

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.user_repository.get_user(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if user.email:
            existing_user = self.user_repository.get_user_by_email(user.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
                
        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: int):
        db_user = self.user_repository.get_user(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return self.user_repository.delete_user(user_id)