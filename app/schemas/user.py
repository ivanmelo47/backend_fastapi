from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re

class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="Nombre de usuario obligatorio (3-50 caracteres)")
    email: str = Field(..., description="Correo electrónico obligatorio")
    full_name: Optional[str] = Field(None, max_length=100)

    @field_validator('username')
    @classmethod
    def validar_username(cls, v):
        if not v:  # Esto no se ejecutará si el campo falta (Pydantic lo maneja antes)
            raise ValueError("El nombre de usuario no puede estar vacío")
        if len(v) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        return v

    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if not v:  # Esto no se ejecutará si el campo falta
            raise ValueError("El correo electrónico no puede estar vacío")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("El correo electrónico no es válido")
        return v

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