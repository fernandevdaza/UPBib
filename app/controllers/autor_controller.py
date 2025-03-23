from sqlalchemy import text
from app.models.database import get_db_connection
from fastapi import HTTPException
from datetime import date
from pymysql import MySQLError


class AutorController:
    @staticmethod
    def create_autor(nombre: str, apellido: str, fecha_nacimiento: date, db=None) -> dict:
        """Crea un autor con validación y manejo de errores"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            autor = db.execute(
                text("SELECT id_autor FROM Autores WHERE nombre_autor = :nombre AND apellido_autor = :apellido"),
                {"nombre": nombre, "apellido": apellido}
            ).fetchone()

            if autor:
                return {"id_autor": autor.id_autor}  # Retornar ID existente sin error

            if not nombre or not apellido:
                raise HTTPException(status_code=400, detail="Nombre y apellido son requeridos")

            existente = db.execute(
                text("""
                    SELECT 1 FROM Autores 
                    WHERE nombre_autor = :nombre 
                    AND apellido_autor = :apellido
                """),
                {"nombre": nombre, "apellido": apellido}
            ).fetchone()

            if existente:
                raise HTTPException(status_code=409, detail="El autor ya existe")

            result = db.execute(
                text("""
                    INSERT INTO Autores 
                    (nombre_autor, apellido_autor, fecha_nacimiento_autor)
                    VALUES (:nombre, :apellido, :fecha_nacimiento)
                """),
                {"nombre": nombre, "apellido": apellido, "fecha_nacimiento": fecha_nacimiento}
            )

            db.commit()
            return {
                "id_autor": result.lastrowid,
                "nombre": nombre,
                "apellido": apellido,
                "fecha_nacimiento": fecha_nacimiento.isoformat()
            }

        except MySQLError as e:
            db.rollback()
            error_code = e.args[0]

            if error_code == 1406:  # Data too long
                raise HTTPException(400, "El nombre o apellido excede la longitud permitida")

            raise HTTPException(500, f"Error de base de datos: {str(e)}")

        finally:
            db.close()

    @staticmethod
    def get_autores(page: int = 1, limit: int = 100, db=None) -> list:
        """Obtiene autores con paginación"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            offset = (page - 1) * limit
            sql = text("""
                SELECT 
                    id_autor,
                    nombre_autor,
                    apellido_autor,
                    fecha_nacimiento_autor
                FROM Autores
                LIMIT :limit OFFSET :offset
            """)

            autores = db.execute(sql, {"limit": limit, "offset": offset}).fetchall()
            return [dict(autor) for autor in autores]

        except MySQLError as e:
            raise HTTPException(500, f"Error al obtener autores: {str(e)}")
        finally:
            db.close()