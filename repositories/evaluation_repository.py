from database.connection import DatabaseConnection


class EvaluationRepository:

    @staticmethod
    def create_evaluation(id_paciente, id_cuestionario, observacion_general=None):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, None, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO TB_EVALUACIONES
                (
                    ID_PACIENTE,
                    ID_CUESTIONARIO,
                    FECHA_INICIO,
                    FECHA_FIN,
                    ESTADO_EVALUACION,
                    OBSERVACION_GENERAL
                )
                VALUES (%s, %s, NOW(), NOW(), 'COMPLETADA', %s)
            """
            cursor.execute(query, (id_paciente, id_cuestionario, observacion_general))
            connection.commit()

            return True, cursor.lastrowid, "Evaluación guardada"

        except Exception as e:
            connection.rollback()
            print(f"Error al crear evaluación: {e}")
            return False, None, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def save_answers(id_evaluacion, answers):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO TB_RESPUESTAS_USUARIO
                (
                    ID_EVALUACION,
                    ID_PREGUNTA,
                    ID_OPCION,
                    VALOR_OBTENIDO
                )
                VALUES (%s, %s, %s, %s)
            """

            values = [
                (
                    id_evaluacion,
                    answer["id_pregunta"],
                    answer["id_opcion"],
                    answer["valor"]
                )
                for answer in answers
            ]

            cursor.executemany(query, values)
            connection.commit()

            return True, "Respuestas guardadas"

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar respuestas: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def save_result(id_evaluacion, puntaje_total, puntaje_escalado, nivel_resultado, interpretacion, requiere_atencion):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO TB_RESULTADOS_CUESTIONARIO
                (
                    ID_EVALUACION,
                    PUNTAJE_TOTAL,
                    PUNTAJE_ESCALADO,
                    NIVEL_RESULTADO,
                    INTERPRETACION,
                    REQUIERE_ATENCION
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    id_evaluacion,
                    puntaje_total,
                    puntaje_escalado,
                    nivel_resultado,
                    interpretacion,
                    requiere_atencion
                )
            )

            connection.commit()
            return True, "Resultado guardado"

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar resultado: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)