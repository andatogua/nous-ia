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
    def get_latest_recommendations_by_user(user_id, limit=15):
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
                    FECHA_GENERACION,
                    ESTADO
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

    @staticmethod
    def get_recommendations_by_period(user_id, period="month"):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            date_condition = ""
            if period == "today":
                date_condition = "AND DATE(FECHA_GENERACION) = CURDATE()"
            elif period == "week":
                date_condition = "AND FECHA_GENERACION >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
            elif period == "month":
                date_condition = "AND FECHA_GENERACION >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"

            query = f"""
                SELECT
                    ID_RECOMENDACION,
                    TITULO,
                    DESCRIPCION,
                    FECHA_GENERACION,
                    ESTADO
                FROM TB_RECOMENDACIONES
                WHERE ID_USUARIO = %s {date_condition}
                ORDER BY FECHA_GENERACION DESC, ID_RECOMENDACION DESC
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener recomendaciones por período: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_recommendations_for_approval(
        estado=None,
        fecha=None,
        paciente_nombre=None,
        limit=100
    ):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            
            conditions = []
            params = []
            
            if estado:
                conditions.append("r.ESTADO = %s")
                params.append(estado)
            
            if fecha:
                conditions.append("DATE(r.FECHA_GENERACION) = %s")
                params.append(fecha)
            
            if paciente_nombre:
                conditions.append("(u.NOMBRE LIKE %s OR u.APELLIDO LIKE %s)")
                params.append(f"%{paciente_nombre}%")
                params.append(f"%{paciente_nombre}%")
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f"""
                SELECT
                    r.ID_RECOMENDACION,
                    r.TITULO,
                    r.DESCRIPCION,
                    r.FECHA_GENERACION,
                    r.ESTADO,
                    u.ID_USUARIO,
                    u.NOMBRE,
                    u.APELLIDO,
                    u.CORREO
                FROM TB_RECOMENDACIONES r
                INNER JOIN TB_USUARIOS u ON r.ID_USUARIO = u.ID_USUARIO
                WHERE {where_clause}
                ORDER BY r.FECHA_GENERACION DESC
                LIMIT %s
            """
            params.append(limit)
            
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener recomendaciones para aprobación: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def update_recommendation_status(recommendation_id, new_status):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return False, "Error de conexión"
        cursor = None
        try:
            cursor = connection.cursor()
            query = """
                UPDATE TB_RECOMENDACIONES
                SET ESTADO = %s
                WHERE ID_RECOMENDACION = %s
            """
            cursor.execute(query, (new_status, recommendation_id))
            connection.commit()
            return True, "Estado actualizado correctamente"
        except Exception as e:
            connection.rollback()
            print(f"Error al actualizar estado: {e}")
            return False, str(e)
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def update_recommendations_by_date(fecha, new_status):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return 0
        cursor = None
        try:
            cursor = connection.cursor()
            query = """
                UPDATE TB_RECOMENDACIONES
                SET ESTADO = %s
                WHERE DATE(FECHA_GENERACION) = %s AND ESTADO = 'PENDIENTE'
            """
            cursor.execute(query, (new_status, fecha))
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            print(f"Error al actualizar estado por fecha: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_recommendation_detail(recommendation_id):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return None
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    r.ID_RECOMENDACION,
                    r.TITULO,
                    r.DESCRIPCION,
                    r.FECHA_GENERACION,
                    r.ESTADO,
                    u.ID_USUARIO,
                    u.NOMBRE,
                    u.APELLIDO,
                    u.CORREO
                FROM TB_RECOMENDACIONES r
                INNER JOIN TB_USUARIOS u ON r.ID_USUARIO = u.ID_USUARIO
                WHERE r.ID_RECOMENDACION = %s
            """
            cursor.execute(query, (recommendation_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener detalle de recomendación: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_patient_tracking_history(recommendation_id):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    s.FECHA_REGISTRO,
                    e.NOMBRE_EMOCION,
                    s.NIVEL_INTENSIDAD,
                    s.OBSERVACION,
                    s.REALIZADA
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD s
                INNER JOIN TB_EMOCIONES e ON s.ID_EMOCION = e.ID_EMOCION
                WHERE s.ID_RECOMENDACION = %s
                ORDER BY s.FECHA_REGISTRO DESC
            """
            cursor.execute(query, (recommendation_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial de seguimiento: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)