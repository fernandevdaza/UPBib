from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str

class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: str
    email: str
    password: str
    codigo_upb: int