from database.connection import DatabaseConnection


class ProfileRepository:

    @staticmethod
    def get_user_profile(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    u.ID_USUARIO,
                    u.CEDULA,
                    u.NOMBRE,
                    u.APELLIDO,
                    u.CORREO,
                    u.TELEFONO,
                    u.USERNAME,
                    u.FECHA_NACIMIENTO,
                    s.DESCRIPCION AS SEXO,
                    r.NOMBRE_ROL
                FROM TB_USUARIOS u
                INNER JOIN TB_SEXOS s
                    ON u.ID_SEXO = s.ID_SEXO
                INNER JOIN TB_ROLES r
                    ON u.ID_ROL = r.ID_ROL
                WHERE u.ID_USUARIO = %s
                LIMIT 1
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener perfil: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def update_user_profile(user_id, nombre, apellido, telefono, username):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                UPDATE TB_USUARIOS
                SET
                    NOMBRE = %s,
                    APELLIDO = %s,
                    TELEFONO = %s,
                    USERNAME = %s,
                    FECHA_ACTUALIZACION = NOW()
                WHERE ID_USUARIO = %s
            """

            cursor.execute(query, (nombre, apellido, telefono, username, user_id))
            connection.commit()

            return True, "Perfil actualizado correctamente."

        except Exception as e:
            connection.rollback()
            print(f"Error al actualizar perfil: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)