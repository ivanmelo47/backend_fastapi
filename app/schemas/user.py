from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)  # Añade validaciones
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(  # Añade el campo username
        None, 
        min_length=3, 
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$"  # Solo caracteres alfanuméricos y guiones bajos
    )
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6)

    @field_validator('username')
    def username_not_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Username no puede estar vacío")
        return v

class UserInDB(UserBase):
    id: int
    uuid: str
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
    
class UserOut(UserBase):
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True