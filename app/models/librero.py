from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Librero(Base):
    __tablename__ = "Libreros"

    id_librero = Column(Integer, primary_key=True, autoincrement=True)
    Usuarios_id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="librero")
    libros = relationship("LibreroLibro", back_populates="librero", cascade="all, delete-orphan")
