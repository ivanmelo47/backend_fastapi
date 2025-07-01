# app/services/auth.py

from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status
from app.models.user import User
from app.models.token import Token
from sqlalchemy.orm import Session
from app.core.security import verify_password
import os
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def autenticar_usuario(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def crear_token_para_usuario(db: Session, user: User):
    # Verifica si hay un token activo
    token_existente = (
        db.query(Token)
        .filter(Token.user_id == user.id, Token.revocado == False, Token.expirado_en > datetime.utcnow())
        .first()
    )
    if token_existente:
        return token_existente.token

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": str(user.id),
        "rol": user.rol,
        "exp": expire.timestamp()
    }
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    nuevo_token = Token(
        user_id=user.id,
        token=encoded_jwt,
        expirado_en=expire,
        revocado=False,
    )
    db.add(nuevo_token)
    db.commit()
    db.refresh(nuevo_token)

    return encoded_jwt
