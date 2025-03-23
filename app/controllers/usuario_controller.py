from sqlalchemy import text
from app.models.database import get_db_connection
from fastapi import HTTPException
from typing import Optional, Dict


class UsuarioController:
    @staticmethod
    def get_usuario(id_usuario: int, db=None) -> Optional[Dict]:
        if db is None:
            db = get_db_connection()
        try:
            sql = text(
                """
                SELECT
                    id_usuario, 
                    nombre_usuario, 
                    apellido_usuario, 
                    email_usuario, 
                    fecha_registro_usuario
                FROM Usuarios 
                WHERE id_usuario = :id_usuario
                """
            )
            result = db.execute(sql, {"id_usuario": id_usuario}).fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            return dict(result)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def delete_usuario(id_usuario: int, db=None) -> Dict:
        if db is None:
            db = get_db_connection()
        try:
            db.begin()

            check_sql = text("SELECT 1 FROM Usuarios WHERE id_usuario = :id_usuario")
            exists = db.execute(check_sql, {"id_usuario": id_usuario}).fetchone()

            if not exists:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            delete_sql = text("DELETE FROM Usuarios WHERE id_usuario = :id_usuario")
            result = db.execute(delete_sql, {"id_usuario": id_usuario})
            db.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="No se pudo eliminar el usuario")

            return {"message": "Usuario eliminado correctamente"}

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")
        finally:
            db.close()