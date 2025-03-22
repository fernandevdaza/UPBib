from typing import Dict
from pymysql import MySQLError
from sqlalchemy import text
from datetime import date
from app.models.database import get_db_connection
from fastapi import HTTPException
from app.controllers.autor_controller import AutorController
from app.controllers.categoria_controller import CategoriaController
from app.controllers.edicion_controller import EdicionController


class LibroController:
    @staticmethod
    def crear_libro_base(
            titulo: str,
            descripcion: str,
            fecha_publicacion: date,
            imagen_url: str,
            db=None
    ) -> Dict:
        """Crea solo el libro base sin ediciones"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            libro_id = db.execute(
                text("""
                    INSERT INTO Libros
                    (titulo_libro, descripcion_libro, imagen_libro, fecha_publicacion_libro)
                    VALUES (:titulo, :descripcion, :imagen, :fecha_publicacion)
                """),
                {
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "imagen": imagen_url,
                    "fecha_publicacion": fecha_publicacion
                }
            ).lastrowid
            db.commit()
            return {
                "id_libro": libro_id,
                "mensaje": "Libro base creado exitosamente"
            }
        except MySQLError as e:
            db.rollback()
            raise HTTPException(500, f"Error al crear libro base: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def crear_libro_completo(
            titulo: str,
            descripcion: str,
            fecha_publicacion: date,
            imagen_url: str,
            autores: list,
            categorias: list,
            ediciones: list,
            db=None
    ) -> Dict:
        """Crea libro con todas sus relaciones en transacción atómica"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            libro_data = {
                "titulo": titulo,
                "descripcion": descripcion,
                "imagen": imagen_url,
                "fecha_publicacion": fecha_publicacion
            }
            libro_id = db.execute(
                text("""
                    INSERT INTO Libros
                    (titulo_libro, descripcion_libro, imagen_libro, fecha_publicacion_libro)
                    VALUES (:titulo, :descripcion, :imagen, :fecha_publicacion)
                """),
                libro_data
            ).lastrowid

            for edicion in ediciones:
                EdicionController.crear_edicion(
                    libro_id=libro_id,
                    isbn=edicion["isbn"],
                    enlace=edicion["enlace"],
                    fecha_edicion=edicion["fecha_edicion"],
                    db=db
                )

            for autor in autores:
                autor_creado = AutorController.create_autor(
                    nombre=autor["nombre"],
                    apellido=autor["apellido"],
                    fecha_nacimiento=autor.get("fecha_nacimiento", "1900-01-01"),
                    db=db
                )
                db.execute(
                    text("""
                        INSERT IGNORE INTO Libros_Autores
                        (libros_id_libro, autores_id_autor)
                        VALUES (:libro_id, :autor_id)
                    """),
                    {"libro_id": libro_id, "autor_id": autor_creado["id_autor"]}
                )

            for categoria in categorias:
                categoria_creada = CategoriaController.create_categoria(
                    nombre=categoria,
                    db=db
                )
                db.execute(
                    text("""
                        INSERT IGNORE INTO Libros_Categorias
                        (libros_id_libro, categorias_id_categoria)
                        VALUES (:libro_id, :categoria_id)
                    """),
                    {"libro_id": libro_id, "categoria_id": categoria_creada["id_categoria"]}
                )

            db.commit()
            return {
                "id_libro": libro_id,
                "mensaje": "Libro completo creado exitosamente",
                "ediciones": [e["id_edicion"] for e in ediciones]
            }
        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error general al crear libro: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def obtener_libro(id_libro: int, db=None) -> Dict:
        """Obtiene un libro con toda su información relacionada"""
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            libro = db.execute(
                text("""
                    SELECT
                        id_libro,
                        titulo_libro,
                        descripcion_libro,
                        imagen_libro,
                        fecha_publicacion_libro
                    FROM Libros
                    WHERE id_libro = :id_libro
                """),
                {"id_libro": id_libro}
            ).fetchone()

            if not libro:
                raise HTTPException(404, "Libro no encontrado")

            libro_dict = libro._asdict()

            autores_result = db.execute(
                text("""
                    SELECT a.id_autor, a.nombre_autor, a.apellido_autor
                    FROM Libros_Autores la
                    JOIN Autores a ON la.autores_id_autor = a.id_autor
                    WHERE la.libros_id_libro = :id_libro
                """),
                {"id_libro": id_libro}
            ).fetchall()
            libro_dict["autores"] = [autor._asdict() for autor in autores_result]

            # Categorías con ._asdict()
            categorias_result = db.execute(
                text("""
                    SELECT c.id_categoria, c.nombre_categoria
                    FROM Libros_Categorias lc
                    JOIN Categorias c ON lc.categorias_id_categoria = c.id_categoria
                    WHERE lc.libros_id_libro = :id_libro
                """),
                {"id_libro": id_libro}
            ).fetchall()
            libro_dict["categorias"] = [cat._asdict() for cat in categorias_result]

            # Ediciones con ._asdict() desde el controlador
            libro_dict["ediciones"] = EdicionController.obtener_ediciones_libro(id_libro)

            return libro_dict
        except MySQLError as e:
            raise HTTPException(500, f"Error al obtener libro: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def get_libros_paginados(page: int = 1, limit: int = 50, db=None):
        offset = (page - 1) * limit
        if db is None:
            db = get_db_connection()
            db.begin()
        try:
            sql = text("""
                WITH ultima_edicion AS (
                    SELECT
                        e.libros_id_libro,
                        e.fecha_edicion,
                        e.enlace_libro,
                        ROW_NUMBER() OVER (
                            PARTITION BY e.libros_id_libro
                            ORDER BY e.fecha_edicion DESC
                        ) AS rn
                    FROM Ediciones e
                )
                SELECT
                    l.id_libro,
                    ANY_VALUE(l.titulo_libro) AS titulo_libro,
                    ANY_VALUE(l.imagen_libro) AS imagen_libro,
                    ANY_VALUE(le.enlace_libro) AS enlace_lectura,
                    GROUP_CONCAT(DISTINCT CONCAT(a.nombre_autor, ' ', a.apellido_autor)) AS autores,
                    GROUP_CONCAT(DISTINCT c.nombre_categoria) AS categorias
                FROM Libros l
                INNER JOIN ultima_edicion le
                    ON l.id_libro = le.libros_id_libro
                    AND le.rn = 1
                LEFT JOIN Libros_Autores la ON l.id_libro = la.libros_id_libro
                LEFT JOIN Autores a ON la.autores_id_autor = a.id_autor
                LEFT JOIN Libros_Categorias lc ON l.id_libro = lc.libros_id_libro
                LEFT JOIN Categorias c ON lc.categorias_id_categoria = c.id_categoria
                GROUP BY l.id_libro
                LIMIT :limit
                OFFSET :offset
            """)
            result = db.execute(sql, {"limit": limit, "offset": offset})
            libros = [row._asdict() for row in result]  # Conversión segura
            return libros
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()