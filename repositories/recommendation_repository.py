from database.connection import DatabaseConnection


class RecommendationRepository:

    @staticmethod
    def get_latest_evaluation_results(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    c.CODIGO,
                    r.ID_RESULTADO,
                    r.PUNTAJE_TOTAL,
                    r.PUNTAJE_ESCALADO,
                    r.NIVEL_RESULTADO,
                    r.INTERPRETACION,
                    e.FECHA_FIN
                FROM TB_EVALUACIONES e
                INNER JOIN TB_PACIENTES p
                    ON e.ID_PACIENTE = p.ID_PACIENTE
                INNER JOIN TB_CUESTIONARIOS c
                    ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
                INNER JOIN TB_RESULTADOS_CUESTIONARIO r
                    ON e.ID_EVALUACION = r.ID_EVALUACION
                WHERE p.ID_USUARIO = %s
                ORDER BY e.FECHA_FIN DESC, e.ID_EVALUACION DESC
            """

            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            latest = {}
            for row in rows:
                code = row["CODIGO"]
                if code not in latest:
                    latest[code] = row

            return latest

        except Exception as e:
            print(f"Error al obtener últimos resultados: {e}")
            return {}

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_latest_mood(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
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
                LIMIT 1
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener último estado emocional: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def save_recommendation(id_resultado, id_usuario, titulo, descripcion):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO TB_RECOMENDACIONES
                (
                    ID_RESULTADO,
                    ID_USUARIO,
                    FUENTE_RECOMENDACION,
                    TITULO,
                    DESCRIPCION
                )
                VALUES (%s, %s, 'GPT', %s, %s)
            """

            cursor.execute(query, (id_resultado, id_usuario, titulo, descripcion))
            connection.commit()

            return True, "Recomendación guardada"

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar recomendación: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_latest_recommendations_by_user(user_id, limit=3):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    ID_RECOMENDACION,
                    TITULO,
                    DESCRIPCION,
                    FECHA_GENERACION
                FROM TB_RECOMENDACIONES
                WHERE ID_USUARIO = %s
                ORDER BY FECHA_GENERACION DESC, ID_RECOMENDACION DESC
                LIMIT %s
            """

            cursor.execute(query, (user_id, limit))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener recomendaciones recientes: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)