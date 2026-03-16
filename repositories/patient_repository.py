from database.connection import DatabaseConnection


class PatientRepository:

    @staticmethod
    def get_patient_by_user_id(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM TB_PACIENTES
                WHERE ID_USUARIO = %s
                LIMIT 1
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener paciente por usuario: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)