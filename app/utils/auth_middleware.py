from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_util import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return payload  # Si el token es válido, se retorna el payload del usuario
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
