from database.connection import DatabaseConnection


class QuestionnaireRepository:

    @staticmethod
    def get_questionnaire_by_code(code):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM TB_CUESTIONARIOS
                WHERE CODIGO = %s AND ACTIVO = 1
                LIMIT 1
            """
            cursor.execute(query, (code,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener cuestionario: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_questions_by_questionnaire(questionnaire_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM TB_PREGUNTAS
                WHERE ID_CUESTIONARIO = %s AND ACTIVA = 1
                ORDER BY ORDEN_PREGUNTA
            """
            cursor.execute(query, (questionnaire_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_options_by_questionnaire(questionnaire_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM TB_OPCIONES_RESPUESTA
                WHERE ID_CUESTIONARIO = %s
                ORDER BY ORDEN_OPCION
            """
            cursor.execute(query, (questionnaire_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener opciones: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)