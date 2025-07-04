# app/schemas/login.py

from pydantic import BaseModel, field_validator
from app.core.validators import validate_not_empty, validate_length, validate_length_A, validate_email_format

class LoginRequest(BaseModel):
    email: str
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = validate_not_empty(v, "correo electrónico")
        return validate_email_format(v)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
