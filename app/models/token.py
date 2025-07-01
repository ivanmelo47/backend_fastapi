from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(512), unique=True, index=True, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    expirado_en = Column(DateTime(timezone=True), nullable=False)
    revocado = Column(Boolean, default=False)

    # Relación inversa con el usuario
    usuario = relationship("app.models.user.User", back_populates="tokens")
