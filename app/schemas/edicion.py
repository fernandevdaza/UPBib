from datetime import date
from pydantic import BaseModel

class EdicionCreate(BaseModel):
    isbn: str
    enlace: str
    fecha_edicion: date
