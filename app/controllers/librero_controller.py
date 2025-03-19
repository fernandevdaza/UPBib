from sqlalchemy import text
from app.models.database import get_db_connection

class LibreroController:

    @staticmethod
    def agregar_libro_librero(id_usuario, id_libro):
        db = get_db_connection()
        try:
            sql_count = text("""
                SELECT COUNT(*) as total FROM Libreros_Libros 
                INNER JOIN Libreros ON Libreros.id_librero = Libreros_Libros.libreros_id_librero 
                WHERE Libreros.Usuarios_id_usuario = :id_usuario
            """)
            total = db.execute(sql_count, {"id_usuario": id_usuario}).scalar()

            if total >= 5:
                return {"error": "No puedes tener más de 5 libros en tu librero"}

            sql_librero = text("SELECT id_librero FROM Libreros WHERE Usuarios_id_usuario = :id_usuario")
            librero = db.execute(sql_librero, {"id_usuario": id_usuario}).fetchone()

            if not librero:
                return {"error": "No se encontró el librero del usuario"}

            sql_insert = text("INSERT INTO Libreros_Libros (libreros_id_librero, libros_id_libro) VALUES (:librero, :libro)")
            db.execute(sql_insert, {"librero": librero.id_librero, "libro": id_libro})
            db.commit()

            return {"message": "Libro agregado al librero correctamente"}
        finally:
            db.close()

    @staticmethod
    def eliminar_libro_librero(id_usuario, id_libro):
        db = get_db_connection()
        try:
            sql = text("""
                DELETE FROM Libreros_Libros 
                WHERE libreros_id_librero = (SELECT id_librero FROM Libreros WHERE Usuarios_id_usuario = :id_usuario) 
                AND libros_id_libro = :id_libro
            """)
            db.execute(sql, {"id_usuario": id_usuario, "id_libro": id_libro})
            db.commit()

            return {"message": "Libro eliminado del librero"}
        finally:
            db.close()
