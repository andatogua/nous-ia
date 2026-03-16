from database.connection import DatabaseConnection


class ReportRepository:

    @staticmethod
    def get_progress_data(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    c.CODIGO,
                    c.NOMBRE AS CUESTIONARIO,
                    e.FECHA_FIN,
                    r.PUNTAJE_TOTAL,
                    r.PUNTAJE_ESCALADO,
                    r.NIVEL_RESULTADO,
                    r.INTERPRETACION
                FROM TB_EVALUACIONES e
                INNER JOIN TB_PACIENTES p
                    ON e.ID_PACIENTE = p.ID_PACIENTE
                INNER JOIN TB_CUESTIONARIOS c
                    ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
                INNER JOIN TB_RESULTADOS_CUESTIONARIO r
                    ON e.ID_EVALUACION = r.ID_EVALUACION
                WHERE p.ID_USUARIO = %s
                ORDER BY e.FECHA_FIN ASC, e.ID_EVALUACION ASC
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener datos de progreso: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)