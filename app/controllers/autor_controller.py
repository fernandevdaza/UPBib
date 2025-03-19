from sqlalchemy import text
from app.models.database import get_db_connection

class AutorController:

    @staticmethod
    def create_autor(nombre, apellido, fecha_nacimiento):
        db = get_db_connection()
        try:
            sql = text("INSERT INTO Autores (nombre_autor, apellido_autor, fecha_nacimiento_autor) VALUES (:nombre, :apellido, :fecha_nacimiento)")
            result = db.execute(sql, {"nombre": nombre, "apellido": apellido, "fecha_nacimiento": fecha_nacimiento})
            db.commit()
            return {"id_autor": result.lastrowid, "nombre": nombre, "apellido": apellido}
        finally:
            db.close()

    @staticmethod
    def get_autores():
        db = get_db_connection()
        try:
            sql = text("SELECT * FROM Autores")
            autores = db.execute(sql).fetchall()
            return [dict(row) for row in autores]
        finally:
            db.close()
