from http.client import HTTPException
from sqlalchemy import text
from app.models.database import get_db_connection

class LibreroController:

    @staticmethod
    def agregar_libro_librero(id_usuario: int, id_libro: int, db=None) -> dict:
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            sql_count = text("""
                SELECT COUNT(*) as total
                FROM Libreros_Libros
                WHERE libreros_id_librero = (
                    SELECT id_librero FROM Libreros
                    WHERE Usuarios_id_usuario = :id_usuario
                )
            """)
            total = db.execute(sql_count, {"id_usuario": id_usuario}).scalar()

            if total >= 5:
                raise HTTPException(400, "Límite de 5 libros alcanzado")

            libro_existe = db.execute(
                text("SELECT 1 FROM Libros WHERE id_libro = :id_libro"),
                {"id_libro": id_libro}
            ).fetchone()

            if not libro_existe:
                raise HTTPException(404, "Libro no encontrado")

            sql_librero = text("SELECT id_librero FROM Libreros WHERE Usuarios_id_usuario = :id_usuario")
            librero = db.execute(sql_librero, {"id_usuario": id_usuario}).fetchone()

            if not librero:
                db.execute(
                    text("INSERT INTO Libreros (Usuarios_id_usuario) VALUES (:id_usuario)"),
                    {"id_usuario": id_usuario}
                )
                librero_id = db.lastrowid
            else:
                librero_id = librero.id_librero

            db.execute(
                text("""
                    INSERT INTO Libreros_Libros (libreros_id_librero, libros_id_libro)
                    VALUES (:librero_id, :libro_id)
                """),
                {"librero_id": librero_id, "libro_id": id_libro}
            )

            db.commit()
            return {"message": "Libro agregado al librero correctamente"}

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error al agregar libro: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def eliminar_libro_librero(id_usuario: int, id_libro: int, db=None) -> dict:
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            result = db.execute(
                text("""
                    DELETE FROM Libreros_Libros
                    WHERE libreros_id_librero = (
                        SELECT id_librero FROM Libreros
                        WHERE Usuarios_id_usuario = :id_usuario
                    )
                    AND libros_id_libro = :id_libro
                """),
                {"id_usuario": id_usuario, "id_libro": id_libro}
            )

            if result.rowcount == 0:
                raise HTTPException(404, "Libro no encontrado en el librero")

            db.commit()
            return {"message": "Libro eliminado del librero exitosamente"}

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error al eliminar libro: {str(e)}")
        finally:
            db.close()
    @staticmethod
    def obtener_libros_librero(id_usuario: int, db=None) -> list:
        """Obtiene los libros en el librero del usuario con información completa"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            sql = text("""
                SELECT 
                    l.id_libro,
                    l.titulo_libro,
                    l.descripcion_libro,
                    l.imagen_libro,
                    e.enlace_libro,
                    e.isbn,
                    GROUP_CONCAT(DISTINCT CONCAT(a.nombre_autor, ' ', a.apellido_autor)) AS autores,
                    GROUP_CONCAT(DISTINCT c.nombre_categoria) AS categorias
                FROM Libreros_Libros ll
                INNER JOIN Libros l ON ll.libros_id_libro = l.id_libro
                INNER JOIN Ediciones e ON l.id_libro = e.libros_id_libro
                LEFT JOIN Libros_Autores la ON l.id_libro = la.libros_id_libro
                LEFT JOIN Autores a ON la.autores_id_autor = a.id_autor
                LEFT JOIN Libros_Categorias lc ON l.id_libro = lc.libros_id_libro
                LEFT JOIN Categorias c ON lc.categorias_id_categoria = c.id_categoria
                WHERE ll.libreros_id_librero = (
                    SELECT id_librero FROM Libreros WHERE Usuarios_id_usuario = :id_usuario
                )
                GROUP BY l.id_libro
                LIMIT 5
            """)

            libros = db.execute(sql, {"id_usuario": id_usuario}).fetchall()
            return [dict(libro) for libro in libros]

        except Exception as e:
            raise HTTPException(500, detail=f"Error obteniendo librero: {str(e)}")
        finally:
            db.close()