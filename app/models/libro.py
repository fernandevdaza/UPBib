from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from .database import Base


class Libro(Base):
    __tablename__ = "Libros"

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    titulo_libro = Column(String(100), nullable=False)
    descripcion_libro = Column(Text, nullable=False)
    imagen_libro = Column(Text, nullable=False)
    fecha_publicacion_libro = Column(Date, nullable=False)

    ediciones = relationship("Edicion", back_populates="libro", cascade="all, delete-orphan")
    autores = relationship("LibroAutor", back_populates="libro", cascade="all, delete-orphan")
    categorias = relationship("LibroCategoria", back_populates="libro", cascade="all, delete-orphan")
