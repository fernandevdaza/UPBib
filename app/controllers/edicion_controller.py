from sqlalchemy import text
from app.models.database import get_db_connection
from fastapi import HTTPException
from typing import Optional, Dict, List
from pymysql import MySQLError


class EdicionController:
    @staticmethod
    def crear_edicion(
            libro_id: int,
            isbn: str,
            enlace: str,
            fecha_edicion: str,
            db=None
    ) -> Dict:
        """Crea una nueva edición para un libro"""
        local_connection = False
        try:
            if db is None:
                db = get_db_connection()
                local_connection = True
                db.begin()

            existente = db.execute(
                text("SELECT 1 FROM Ediciones WHERE isbn = :isbn"),
                {"isbn": isbn}
            ).fetchone()

            if existente:
                raise HTTPException(400, "ISBN ya registrado")

            result = db.execute(
                text("""
                    INSERT INTO Ediciones 
                    (libros_id_libro, isbn, enlace_libro, fecha_edicion)
                    VALUES (:libro_id, :isbn, :enlace, :fecha_edicion)
                """),
                {
                    "libro_id": libro_id,
                    "isbn": isbn,
                    "enlace": enlace,
                    "fecha_edicion": fecha_edicion
                }
            )

            if local_connection:
                db.commit()

            return {
                "id_edicion": result.lastrowid,
                "mensaje": "Edición creada exitosamente"
            }

        except MySQLError as e:
            if local_connection and db:
                db.rollback()
            error_code = e.args[0]
            if error_code == 1452:
                raise HTTPException(404, "Libro no encontrado")
            raise HTTPException(500, f"Error de base de datos: {str(e)}")
        finally:
            if local_connection and db:
                db.close()

    @staticmethod
    def obtener_ediciones_libro(libro_id: int, db=None) -> List[Dict]:
        """Obtiene todas las ediciones de un libro"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            ediciones = db.execute(
                text("SELECT * FROM Ediciones WHERE libros_id_libro = :libro_id"),
                {"libro_id": libro_id}
            ).fetchall()

            return [edicion._asdict() for edicion in ediciones]

        except MySQLError as e:
            raise HTTPException(500, f"Error al obtener ediciones: {str(e)}")
        finally:
            db.close()