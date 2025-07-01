# app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.login import LoginRequest, LoginResponse
from app.services.auth import autenticar_usuario, crear_token_para_usuario

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token_para_usuario(db, user)
    return {"access_token": token}
