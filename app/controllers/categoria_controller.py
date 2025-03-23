from sqlalchemy import text
from app.models.database import get_db_connection
from fastapi import HTTPException
from pymysql import MySQLError


class CategoriaController:
    @staticmethod
    def create_categoria(nombre: str, db=None) -> dict:
        """Crea categoría con manejo de duplicados"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            result = db.execute(
                text("SELECT id_categoria FROM Categorias WHERE nombre_categoria = :nombre"),
                {"nombre": nombre}
            ).fetchone()

            if result:
                return {"id_categoria": result[0]}

            result = db.execute(
                text("INSERT INTO Categorias (nombre_categoria) VALUES (:nombre)"),
                {"nombre": nombre}
            )
            db.commit()
            return {"id_categoria": result.lastrowid}

        except MySQLError as e:
            db.rollback()
            error_code = e.args[0]

            if error_code == 1062:
                raise HTTPException(409, "La categoría ya existe")

            raise HTTPException(500, f"Error de base de datos: {str(e)}")

        finally:
            db.close()

    @staticmethod
    def get_categorias(search: str = None, db=None) -> list:
        """Obtiene categorías con filtro de búsqueda"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            sql_query = """
                    SELECT 
                        id_categoria,
                        nombre_categoria
                    FROM Categorias
                """
            params = {}

            if search:
                sql_query += " WHERE nombre_categoria LIKE :search"
                params["search"] = f"%{search}%"

            categorias = db.execute(text(sql_query), params).fetchall()
            return [dict(categoria) for categoria in categorias]

        except MySQLError as e:
            raise HTTPException(500, f"Error al obtener categorías: {str(e)}")
        finally:
            db.close()