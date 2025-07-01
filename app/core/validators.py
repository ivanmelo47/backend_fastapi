# app/core/validators.py

from typing import Optional
import re

def validate_not_empty(v: str, field_name: str) -> str:
    """Valida que un campo string no esté vacío después de eliminar espacios"""
    v = v.strip()
    if not v:
        raise ValueError(f"El {field_name} no puede estar vacío")
    return v

def validate_length(v: str, field_name: str, 
                  min_len: Optional[int] = None, 
                  max_len: Optional[int] = None) -> str:
    """Valida la longitud mínima y máxima de un string"""
    if min_len is not None and len(v) < min_len:
        raise ValueError(f"El {field_name} debe tener al menos {min_len} caracteres")
    if max_len is not None and len(v) > max_len:
        raise ValueError(f"El {field_name} no debe exceder {max_len} caracteres")
    return v

def validate_length_A(v: str, field_name: str, 
                  min_len: Optional[int] = None, 
                  max_len: Optional[int] = None) -> str:
    """Valida la longitud mínima y máxima de un string"""
    if min_len is not None and len(v) < min_len:
        raise ValueError(f"La {field_name} debe tener al menos {min_len} caracteres")
    if max_len is not None and len(v) > max_len:
        raise ValueError(f"La {field_name} no debe exceder {max_len} caracteres")
    return v

def validate_email_format(v: str) -> str:
    """Valida el formato básico de un email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
        raise ValueError("El correo electrónico no es válido")
    return v