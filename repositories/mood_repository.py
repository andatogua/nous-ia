from database.connection import DatabaseConnection


class MoodRepository:

    @staticmethod
    def save_mood_record(id_paciente, id_emocion, nivel_intensidad, observacion):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO TB_REGISTROS_ESTADO_ANIMO
                (
                    ID_PACIENTE,
                    ID_EMOCION,
                    NIVEL_INTENSIDAD,
                    OBSERVACION,
                    FECHA_REGISTRO
                )
                VALUES (%s, %s, %s, %s, NOW())
            """

            cursor.execute(query, (id_paciente, id_emocion, nivel_intensidad, observacion))
            connection.commit()

            return True, "Registro emocional guardado correctamente."

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar estado de ánimo: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_mood_history_by_user(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    r.ID_REGISTRO_ANIMO,
                    e.NOMBRE_EMOCION,
                    r.NIVEL_INTENSIDAD,
                    r.OBSERVACION,
                    r.FECHA_REGISTRO
                FROM TB_REGISTROS_ESTADO_ANIMO r
                INNER JOIN TB_PACIENTES p
                    ON r.ID_PACIENTE = p.ID_PACIENTE
                INNER JOIN TB_EMOCIONES e
                    ON r.ID_EMOCION = e.ID_EMOCION
                WHERE p.ID_USUARIO = %s
                ORDER BY r.FECHA_REGISTRO DESC, r.ID_REGISTRO_ANIMO DESC
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener historial emocional: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)