from database.connection import DatabaseConnection


class ActivityEmotionalTrackingRepository:

    @staticmethod
    def save_activity_emotional_tracking(
        user_id,
        id_recomendacion,
        id_emocion,
        nivel_intensidad,
        observacion,
        realizada
    ):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            check_query = """
                SELECT ID_SEGUIMIENTO_ACTIVIDAD
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD
                WHERE ID_USUARIO = %s AND ID_RECOMENDACION = %s
                LIMIT 1
            """
            cursor.execute(check_query, (user_id, id_recomendacion))
            existing = cursor.fetchone()

            if existing:
                return False, "Esta actividad ya fue registrada previamente."

            insert_query = """
                INSERT INTO TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD
                (
                    ID_USUARIO,
                    ID_RECOMENDACION,
                    ID_EMOCION,
                    NIVEL_INTENSIDAD,
                    OBSERVACION,
                    REALIZADA,
                    FECHA_REGISTRO
                )
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(
                insert_query,
                (
                    user_id,
                    id_recomendacion,
                    id_emocion,
                    nivel_intensidad,
                    observacion,
                    realizada
                )
            )

            connection.commit()
            return True, "Seguimiento emocional de la actividad guardado correctamente."

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar seguimiento emocional por actividad: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def exists_activity_emotional_tracking(user_id, id_recomendacion):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT ID_SEGUIMIENTO_ACTIVIDAD
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD
                WHERE ID_USUARIO = %s AND ID_RECOMENDACION = %s
                LIMIT 1
            """
            cursor.execute(query, (user_id, id_recomendacion))
            result = cursor.fetchone()

            return result is not None

        except Exception as e:
            print(f"Error al verificar seguimiento emocional por actividad: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_registered_activity_ids(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT ID_RECOMENDACION
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD
                WHERE ID_USUARIO = %s
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            return [row["ID_RECOMENDACION"] for row in rows]

        except Exception as e:
            print(f"Error al obtener actividades ya registradas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def get_activity_emotional_tracking_by_user(user_id):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    s.ID_RECOMENDACION,
                    s.ID_EMOCION,
                    e.NOMBRE_EMOCION,
                    s.NIVEL_INTENSIDAD,
                    s.OBSERVACION,
                    s.REALIZADA,
                    s.FECHA_REGISTRO
                FROM TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD s
                INNER JOIN TB_EMOCIONES e
                    ON s.ID_EMOCION = e.ID_EMOCION
                WHERE s.ID_USUARIO = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener seguimiento emocional por actividad: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)