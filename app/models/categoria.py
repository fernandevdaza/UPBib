from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Categoria(Base):
    __tablename__ = "Categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(50), unique=True, nullable=False)

    libros = relationship("LibroCategoria", back_populates="categoria", cascade="all, delete-orphan")
    