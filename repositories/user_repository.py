from database.connection import DatabaseConnection


class UserRepository:

    @staticmethod
    def get_user_by_email(email):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM TB_USUARIOS
                WHERE CORREO = %s
                LIMIT 1
            """
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user

        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

        finally:
            cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def create_user(user_data):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query_user = """
                INSERT INTO TB_USUARIOS
                (
                    CEDULA,
                    NOMBRE,
                    APELLIDO,
                    CORREO,
                    TELEFONO,
                    FECHA_NACIMIENTO,
                    ID_SEXO,
                    USERNAME,
                    PASSWORD_HASH,
                    ID_ROL,
                    ESTADO_CUENTA
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values_user = (
                user_data["cedula"],
                user_data["nombre"],
                user_data["apellido"],
                user_data["correo"],
                user_data["telefono"],
                user_data["fecha_nacimiento"],
                user_data["id_sexo"],
                user_data["username"],
                user_data["password_hash"],
                user_data["id_rol"],
                "ACTIVO"
            )

            cursor.execute(query_user, values_user)
            user_id = cursor.lastrowid

            query_patient = """
                INSERT INTO TB_PACIENTES (ID_USUARIO, FECHA_REGISTRO)
                VALUES (%s, NOW())
            """
            cursor.execute(query_patient, (user_id,))

            connection.commit()
            return True, "Usuario registrado correctamente"

        except Exception as e:
            connection.rollback()
            print(f"Error creating user: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)