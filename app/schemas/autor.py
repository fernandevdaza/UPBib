from datetime import date
from pydantic import BaseModel

class AutorCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
