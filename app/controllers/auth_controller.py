from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, UTC
from app.utils.hash_util import verify_password, hash_password
from app.utils.jwt_util import create_access_token, create_refresh_token, decode_refresh_token
from app.models.database import get_db_connection

REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthController:

    @staticmethod
    def login(email: str, password: str):
        db = get_db_connection()
        try:
            db.begin()

            sql = text("SELECT id_usuario, nombre_usuario, email_usuario, contrasenia_usuario FROM Usuarios WHERE email_usuario = :email")
            user = db.execute(sql, {"email": email}).fetchone()

            if not user or not verify_password(password, user.contrasenia_usuario):
                return None

            access_token = create_access_token(
                {"sub": user.email_usuario, "id": user.id_usuario, "nombre": user.nombre_usuario})
            refresh_token = create_refresh_token({"sub": user.email_usuario})
            expira_en = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

            sql_insert = text("INSERT INTO RefreshTokens (usuario_id, token, fecha_expiracion) VALUES (:usuario_id, :token, :fecha_expiracion)")
            db.execute(sql_insert, {"usuario_id": user.id_usuario, "token": refresh_token, "fecha_expiracion": expira_en})
            db.commit()

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        finally:
            db.close()

    @staticmethod
    def refresh_token(refresh_token: str):
        db = get_db_connection()
        try:
            db.begin()

            sql = text("SELECT usuario_id, fecha_expiracion FROM RefreshTokens WHERE token = :token")
            token_data = db.execute(sql, {"token": refresh_token}).fetchone()

            if not token_data:
                return {"error": "Refresh Token inválido o revocado"}

            if token_data.fecha_expiracion < datetime.now(UTC):
                return {"error": "Refresh Token expirado, inicia sesión nuevamente"}

            payload = decode_refresh_token(refresh_token)
            email = payload["sub"]

            new_access_token = create_access_token({"sub": email})
            return {"access_token": new_access_token, "token_type": "bearer"}
        finally:
            db.close()

    @staticmethod
    def logout(refresh_token: str):
        db = get_db_connection()
        try:
            db.begin()
            sql = text("DELETE FROM RefreshTokens WHERE token = :token")
            db.execute(sql, {"token": refresh_token})
            db.commit()
            return {"message": "Sesión cerrada exitosamente"}
        finally:
            db.close()

    @staticmethod
    def limpiar_tokens_expirados():
        db = get_db_connection()
        try:
            db.begin()
            sql = text("DELETE FROM RefreshTokens WHERE fecha_expiracion < NOW()")
            db.execute(sql)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def register(nombre, apellido, fecha_nacimiento, email, password, codigo_upb):
        db = get_db_connection()
        try:
            db.begin()

            sql_email_check = text("SELECT email_usuario FROM Usuarios WHERE email_usuario = :email")
            existing_user = db.execute(sql_email_check, {"email": email}).fetchone()

            if existing_user:
                return {"error": "El email ya está registrado"}

            hashed_password = hash_password(password)

            sql_insert_user = text("""
                INSERT INTO Usuarios (nombre_usuario, apellido_usuario, fecha_nacimiento_usuario, 
                                      email_usuario, contrasenia_usuario, codigo_estudiante_upb)
                VALUES (:nombre, :apellido, :fecha_nacimiento, :email, :hashed_password, :codigo_upb)
            """)
            db.execute(sql_insert_user, {
                "nombre": nombre,
                "apellido": apellido,
                "fecha_nacimiento": fecha_nacimiento,
                "email": email,
                "hashed_password": hashed_password,
                "codigo_upb": codigo_upb
            })
            db.commit()

            sql_get_user = text("SELECT id_usuario FROM Usuarios WHERE email_usuario = :email")
            user = db.execute(sql_get_user, {"email": email}).fetchone()
            usuario_id = user.id_usuario

            sql_insert_librero = text("INSERT INTO Libreros (Usuarios_id_usuario) VALUES (:usuario_id)")
            db.execute(sql_insert_librero, {"usuario_id": usuario_id})
            db.commit()

            access_token = create_access_token({"sub": email, "id": usuario_id, "nombre": nombre})
            refresh_token = create_refresh_token({"sub": email})

            sql_insert_token = text("""
                INSERT INTO RefreshTokens (usuario_id, token, fecha_expiracion) 
                VALUES (:usuario_id, :refresh_token, :fecha_expiracion)
            """)
            expira_en = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            db.execute(sql_insert_token, {"usuario_id": usuario_id, "refresh_token": refresh_token, "fecha_expiracion": expira_en})
            db.commit()

            return {
                "id_usuario": usuario_id,
                "email": email,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        finally:
            db.close()