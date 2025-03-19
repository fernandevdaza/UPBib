from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base


class Autor(Base):
    __tablename__ = "Autores"

    id_autor = Column(Integer, primary_key=True, autoincrement=True)
    nombre_autor = Column(String(50), nullable=False)
    apellido_autor = Column(String(50), nullable=False)
    fecha_nacimiento_autor = Column(Date, nullable=False)

    libros = relationship("LibroAutor", back_populates="autor", cascade="all, delete-orphan")
