from database.connection import DatabaseConnection


class StatisticsRepository:

    @staticmethod
    def get_user_statistics(user_id):

        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None

        try:

            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT
                c.CODIGO,
                r.PUNTAJE_TOTAL,
                r.PUNTAJE_ESCALADO,
                r.NIVEL_RESULTADO,
                e.FECHA_FIN
            FROM TB_EVALUACIONES e
            INNER JOIN TB_PACIENTES p
                ON e.ID_PACIENTE = p.ID_PACIENTE
            INNER JOIN TB_CUESTIONARIOS c
                ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
            INNER JOIN TB_RESULTADOS_CUESTIONARIO r
                ON e.ID_EVALUACION = r.ID_EVALUACION
            WHERE p.ID_USUARIO = %s
            ORDER BY e.FECHA_FIN ASC
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Exception as e:

            print(f"Error obteniendo estadísticas: {e}")
            return []

        finally:

            if cursor:
                cursor.close()

            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_global_patient_count():
        connection = DatabaseConnection.get_connection()
        if not connection:
            return 0
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT COUNT(*) as total FROM TB_USUARIOS WHERE ID_ROL = 2"
            cursor.execute(query)
            result = cursor.fetchone()
            return result["total"] if result else 0
        except Exception as e:
            print(f"Error obteniendo total de pacientes: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_global_recommendation_stats():
        connection = DatabaseConnection.get_connection()
        if not connection:
            return {"total": 0, "pending": 0, "approved": 0, "rejected": 0}
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN ESTADO = 'PENDIENTE' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN ESTADO = 'APROBADO' THEN 1 ELSE 0 END) as approved,
                    SUM(CASE WHEN ESTADO = 'RECHAZADO' THEN 1 ELSE 0 END) as rejected
                FROM TB_RECOMENDACIONES
            """
            cursor.execute(query)
            result = cursor.fetchone()
            return {
                "total": result["total"] or 0,
                "pending": result["pending"] or 0,
                "approved": result["approved"] or 0,
                "rejected": result["rejected"] or 0
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas de recomendaciones: {e}")
            return {"total": 0, "pending": 0, "approved": 0, "rejected": 0}
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_global_evaluation_averages():
        connection = DatabaseConnection.get_connection()
        if not connection:
            return {"avg_phq": 0, "avg_who": 0, "total_evaluations": 0}
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    c.CODIGO,
                    AVG(r.PUNTAJE_TOTAL) as avg_total,
                    AVG(r.PUNTAJE_ESCALADO) as avg_scaled
                FROM TB_EVALUACIONES e
                INNER JOIN TB_CUESTIONARIOS c ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
                INNER JOIN TB_RESULTADOS_CUESTIONARIO r ON e.ID_EVALUACION = r.ID_EVALUACION
                GROUP BY c.CODIGO
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            avg_phq = 0
            avg_who = 0
            total = 0
            
            for row in results:
                if row["CODIGO"] == "PHQ-9":
                    avg_phq = round(row["avg_total"], 2) if row["avg_total"] else 0
                elif row["CODIGO"] == "WHO-5":
                    avg_who = round(row["avg_scaled"], 2) if row["avg_scaled"] else 0
            
            total_query = "SELECT COUNT(*) as total FROM TB_EVALUACIONES"
            cursor.execute(total_query)
            total_result = cursor.fetchone()
            total = total_result["total"] if total_result else 0
            
            return {
                "avg_phq": avg_phq,
                "avg_who": avg_who,
                "total_evaluations": total
            }
        except Exception as e:
            print(f"Error obteniendo promedios de evaluaciones: {e}")
            return {"avg_phq": 0, "avg_who": 0, "total_evaluations": 0}
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_emotions_frequency():
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    e.NOMBRE_EMOCION,
                    COUNT(*) as cantidad
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD s
                INNER JOIN TB_EMOCIONES e ON s.ID_EMOCION = e.ID_EMOCION
                GROUP BY e.NOMBRE_EMOCION
                ORDER BY cantidad DESC
                LIMIT 10
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo frecuencia de emociones: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_activity_completion_rate():
        connection = DatabaseConnection.get_connection()
        if not connection:
            return {"total": 0, "completed": 0, "rate": 0}
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN REALIZADA = 1 THEN 1 ELSE 0 END) as completed
                FROM TB_SEGUIMIENTO_RECOMENDACIONES
            """
            cursor.execute(query)
            result = cursor.fetchone()
            total = result["total"] or 0
            completed = result["completed"] or 0
            rate = round((completed / total) * 100, 2) if total > 0 else 0
            return {
                "total": total,
                "completed": completed,
                "rate": rate
            }
        except Exception as e:
            print(f"Error obteniendo tasa de completitud: {e}")
            return {"total": 0, "completed": 0, "rate": 0}
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_evaluations_by_period(days=30):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = f"""
                SELECT 
                    DATE(e.FECHA_FIN) as fecha,
                    c.CODIGO,
                    COUNT(*) as cantidad,
                    AVG(r.PUNTAJE_TOTAL) as avg_score
                FROM TB_EVALUACIONES e
                INNER JOIN TB_CUESTIONARIOS c ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
                INNER JOIN TB_RESULTADOS_CUESTIONARIO r ON e.ID_EVALUACION = r.ID_EVALUACION
                WHERE e.FECHA_FIN >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                GROUP BY DATE(e.FECHA_FIN), c.CODIGO
                ORDER BY fecha ASC
            """
            cursor.execute(query, (days,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo evaluaciones por período: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_recent_users(limit=10):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    u.ID_USUARIO,
                    u.NOMBRE,
                    u.APELLIDO,
                    u.CORREO,
                    u.FECHA_CREACION,
                    COUNT(DISTINCT e.ID_EVALUACION) as total_evaluaciones,
                    COUNT(DISTINCT r.ID_RECOMENDACION) as total_recomendaciones
                FROM TB_USUARIOS u
                LEFT JOIN TB_PACIENTES p ON u.ID_USUARIO = p.ID_USUARIO
                LEFT JOIN TB_EVALUACIONES e ON p.ID_PACIENTE = e.ID_PACIENTE
                LEFT JOIN TB_RECOMENDACIONES r ON u.ID_USUARIO = r.ID_USUARIO
                WHERE u.ID_ROL = 2
                GROUP BY u.ID_USUARIO
                ORDER BY u.FECHA_CREACION DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo usuarios recientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_all_patients(search_term=None):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            
            base_query = """
                SELECT 
                    u.ID_USUARIO,
                    u.CEDULA,
                    u.NOMBRE,
                    u.APELLIDO,
                    u.CORREO,
                    u.TELEFONO,
                    u.FECHA_NACIMIENTO,
                    s.DESCRIPCION as SEXO,
                    u.FECHA_CREACION,
                    COUNT(DISTINCT e.ID_EVALUACION) as total_evaluaciones,
                    COUNT(DISTINCT r.ID_RECOMENDACION) as total_recomendaciones
                FROM TB_USUARIOS u
                LEFT JOIN TB_SEXOS s ON u.ID_SEXO = s.ID_SEXO
                LEFT JOIN TB_PACIENTES p ON u.ID_USUARIO = p.ID_USUARIO
                LEFT JOIN TB_EVALUACIONES e ON p.ID_PACIENTE = e.ID_PACIENTE
                LEFT JOIN TB_RECOMENDACIONES r ON u.ID_USUARIO = r.ID_USUARIO
            """
            
            if search_term:
                query = base_query + """
                    WHERE u.ID_ROL = 2 
                    AND (u.NOMBRE LIKE %s OR u.APELLIDO LIKE %s OR u.CORREO LIKE %s OR u.CEDULA LIKE %s)
                    GROUP BY u.ID_USUARIO
                    ORDER BY u.FECHA_CREACION DESC
                """
                search_pattern = f"%{search_term}%"
                cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            else:
                query = base_query + """
                    WHERE u.ID_ROL = 2
                    GROUP BY u.ID_USUARIO
                    ORDER BY u.FECHA_CREACION DESC
                """
                cursor.execute(query)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo pacientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_patient_detail(user_id):
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
                    u.FECHA_NACIMIENTO,
                    s.DESCRIPCION as SEXO,
                    u.FECHA_CREACION
                FROM TB_USUARIOS u
                LEFT JOIN TB_SEXOS s ON u.ID_SEXO = s.ID_SEXO
                WHERE u.ID_USUARIO = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error obteniendo detalle del paciente: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_patient_evaluations(user_id):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    c.CODIGO,
                    r.PUNTAJE_TOTAL,
                    r.PUNTAJE_ESCALADO,
                    r.NIVEL_RESULTADO,
                    e.FECHA_FIN
                FROM TB_EVALUACIONES e
                INNER JOIN TB_PACIENTES p ON e.ID_PACIENTE = p.ID_PACIENTE
                INNER JOIN TB_CUESTIONARIOS c ON e.ID_CUESTIONARIO = c.ID_CUESTIONARIO
                INNER JOIN TB_RESULTADOS_CUESTIONARIO r ON e.ID_EVALUACION = r.ID_EVALUACION
                WHERE p.ID_USUARIO = %s
                ORDER BY e.FECHA_FIN DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo evaluaciones del paciente: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_patient_recommendations(user_id):
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
                    ESTADO,
                    FECHA_GENERACION
                FROM TB_RECOMENDACIONES
                WHERE ID_USUARIO = %s
                ORDER BY FECHA_GENERACION DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo recomendaciones del paciente: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_patient_emotional_history(user_id):
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
                    s.REALIZADA,
                    r.TITULO as RECOMENDACION_TITULO
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD s
                INNER JOIN TB_EMOCIONES e ON s.ID_EMOCION = e.ID_EMOCION
                INNER JOIN TB_RECOMENDACIONES r ON s.ID_RECOMENDACION = r.ID_RECOMENDACION
                WHERE s.ID_USUARIO = %s
                ORDER BY s.FECHA_REGISTRO DESC
                LIMIT 50
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo historial emocional: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)