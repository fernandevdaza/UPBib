from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Edicion(Base):
    __tablename__ = "Ediciones"

    id_edicion = Column(Integer, primary_key=True, autoincrement=True)
    libros_id_libro = Column(Integer, ForeignKey("Libros.id_libro"), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    enlace_libro = Column(Text, nullable=False)
    fecha_edicion = Column(Date, nullable=False)

    libro = relationship("Libro", back_populates="ediciones")
