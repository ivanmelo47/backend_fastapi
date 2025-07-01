# app/core/security.py

from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.token import Token
#import os
from app.config import settings
#from app.repositories.user import UserRepository
from app.services.responses import CustomHTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

#SECRET_KEY = os.getenv("SECRET_KEY")
#ALGORITHM = os.getenv("ALGORITHM")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_token = db.query(Token).filter(Token.token == token, Token.revocado == False).first()
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revocado o no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido para administradores"
        )
    return current_user  # 👈 Lo devolvemos por si se quiere usar

def verificar_acceso_usuario(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id == user_id:
        return current_user

    # No validamos si el usuario existe aquí
    # Solo negamos el acceso si no está autorizado
    if current_user.rol == "admin":
        target_user = db.query(User).filter(User.id == user_id).first()
        if target_user and target_user.rol == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "codigo": status.HTTP_403_FORBIDDEN,
                    "mensaje": ["No puedes modificar a otro admin"],
                    "data": None
                }
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "codigo": status.HTTP_403_FORBIDDEN,
                "mensaje": ["No tienes permisos para modificar a otro usuario"],
                "data": None
            }
        )

    return current_user
