from datetime import date
from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nombre: str