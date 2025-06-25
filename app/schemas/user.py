# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re
from app.core.validators import validate_not_empty, validate_length, validate_length_A, validate_email_format

class UserBase(BaseModel):
    username: str = Field(..., description="Nombre de usuario obligatorio (3-50 caracteres)")
    email: str = Field(..., description="Correo electrónico obligatorio")
    full_name: str = Field(..., description="Nombre completo del usuario")

    @field_validator('username')
    @classmethod
    def validar_username(cls, v: str) -> str:
        v = validate_not_empty(v, "nombre de usuario")
        return validate_length(v, "nombre de usuario", min_len=3, max_len=50)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = validate_not_empty(v, "correo electrónico")
        return validate_email_format(v)
    
    @field_validator('full_name')
    @classmethod
    def validar_full_name(cls, v: str) -> str:
        v = validate_not_empty(v, "nombre completo")
        return validate_length(v, "nombre completo", min_len=3, max_len=100)

class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña obligatoria (mín. 6 caracteres)")

    @field_validator('password')
    @classmethod
    def validar_password(cls, v: str) -> str:
        v = validate_not_empty(v, "constraseña")
        return validate_length_A(v, "contraseña", min_len=6, max_len=100)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Nombre de usuario opcional (3-50 caracteres alfanuméricos)")
    email: Optional[str] = Field(None, description="Correo electronico opcional")
    full_name: Optional[str] = Field(None)
    password: Optional[str] = Field(None)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = validate_not_empty(v, "nombre de usuario")
            v = validate_length(v, "nombre de usuario", min_len=3, max_len=50)
            if not re.match(r"^[a-zA-Z0-9_]+$", v):
                raise ValueError("El nombre de usuario no es valido")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = validate_not_empty(v, "correo electrónico")
            v = validate_email_format(v)
        return v
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = validate_not_empty(v, "nombre completo")
            v = validate_length(v, "nombre completo",  min_len=3, max_len=100)
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = validate_not_empty(v, "contraseña")
            v = validate_length_A(v, "contraseña", min_len=6, max_len=100)
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