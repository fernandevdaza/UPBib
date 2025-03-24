from datetime import date
from pydantic import BaseModel

class LibroCreate(BaseModel):
    titulo: str
    descripcion: str
    fecha_publicacion: date
    imagen_url: str
    autores: list[dict]
    categorias: list[str]
    ediciones: list[dict]
