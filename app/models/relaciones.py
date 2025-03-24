from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class LibreroLibro(Base):
    __tablename__ = "Libreros_Libros"

    libreros_id_librero = Column(Integer, ForeignKey("Libreros.id_librero"), primary_key=True)
    libros_id_libro = Column(Integer, ForeignKey("Libros.id_libro"), primary_key=True)

    librero = relationship("Librero", back_populates="libros")
    libro = relationship("Libro")


class LibroAutor(Base):
    __tablename__ = "Libros_Autores"

    libros_id_libro = Column(Integer, ForeignKey("Libros.id_libro"), primary_key=True)
    autores_id_autor = Column(Integer, ForeignKey("Autores.id_autor"), primary_key=True)

    libro = relationship("Libro", back_populates="autores")
    autor = relationship("Autor", back_populates="libros")


class LibroCategoria(Base):
    __tablename__ = "Libros_Categorias"

    libros_id_libro = Column(Integer, ForeignKey("Libros.id_libro"), primary_key=True)
    categorias_id_categoria = Column(Integer, ForeignKey("Categorias.id_categoria"), primary_key=True)

    libro = relationship("Libro", back_populates="categorias")
    categoria = relationship("Categoria", back_populates="libros")
