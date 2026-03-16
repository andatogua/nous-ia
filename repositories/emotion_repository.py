from database.connection import DatabaseConnection


class EmotionRepository:

    @staticmethod
    def get_all_emotions():
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT ID_EMOCION, NOMBRE_EMOCION
                FROM TB_EMOCIONES
                ORDER BY NOMBRE_EMOCION ASC
            """
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener emociones: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)