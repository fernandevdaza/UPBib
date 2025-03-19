from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class Usuario(Base):
    __tablename__ = "Usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(20), nullable=False)
    apellido_usuario = Column(String(20), nullable=False)
    fecha_nacimiento_usuario = Column(Date, nullable=False)
    email_usuario = Column(String(100), unique=True, nullable=False)
    contrasenia_usuario = Column(String(255), nullable=False)
    fecha_registro_usuario = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    codigo_estudiante_upb = Column(Integer, unique=True, nullable=True)

    librero = relationship("Librero", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
