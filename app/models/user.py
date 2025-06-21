from sqlalchemy import Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.mysql import CHAR
import uuid as uuid_lib

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(CHAR(36), default=lambda: str(uuid_lib.uuid4()), unique=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Nuevos campos
    status = Column(Boolean, nullable=False, server_default=text("false"))
    rol = Column(String(20), nullable=False, server_default=text("'user'"))
    deleted_at = Column(DateTime, nullable=True)