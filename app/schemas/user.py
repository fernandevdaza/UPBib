from pydantic import BaseModel


class UsuarioBase(BaseModel):
    email: str
    nombre: str
    apellido: str

class UsuarioCreate(UsuarioBase):
    contrasenia: str
    fecha_nacimiento: date
    codigo_estudiante: int | None = None

class UserLogin(BaseModel):
    email: str
    password: str
