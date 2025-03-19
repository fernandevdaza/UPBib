from pymysql import cursors
from app.models.database import get_db_connection


class UsuarioController:

    @staticmethod
    def get_usuario(id_usuario):
        conn = get_db_connection()
        cursor = conn.cursor(cursors.DictCursor)

        sql = "SELECT * FROM Usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return usuario

    @staticmethod
    def delete_usuario(id_usuario):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM Usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Usuario eliminado correctamente"}
