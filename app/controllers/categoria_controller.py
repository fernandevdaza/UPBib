from sqlalchemy import text
from app.models.database import get_db_connection

class CategoriaController:

    @staticmethod
    def create_categoria(nombre):
        db = get_db_connection()
        try:
            sql = text("INSERT INTO Categorias (nombre_categoria) VALUES (:nombre)")
            result = db.execute(sql, {"nombre": nombre})
            db.commit()
            return {"id_categoria": result.lastrowid, "nombre": nombre}
        finally:
            db.close()

    @staticmethod
    def get_categorias():
        db = get_db_connection()
        try:
            sql = text("SELECT * FROM Categorias")
            categorias = db.execute(sql).fetchall()
            return [dict(row) for row in categorias]
        finally:
            db.close()
