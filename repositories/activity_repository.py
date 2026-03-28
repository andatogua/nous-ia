from database.connection import DatabaseConnection


class ActivityRepository:

    @staticmethod
    def get_latest_recommendations_with_tracking(user_id, limit=15):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

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
                    s.ID_SEGUIMIENTO,
                    s.REALIZADA,
                    s.FECHA_REGISTRO
                FROM TB_RECOMENDACIONES r
                LEFT JOIN TB_SEGUIMIENTO_RECOMENDACIONES s
                    ON r.ID_RECOMENDACION = s.ID_RECOMENDACION
                    AND s.ID_USUARIO = r.ID_USUARIO
                WHERE r.ID_USUARIO = %s
                ORDER BY r.FECHA_GENERACION DESC, r.ID_RECOMENDACION DESC
                LIMIT %s
            """

            cursor.execute(query, (user_id, limit))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener actividades de seguimiento: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)

    @staticmethod
    def save_tracking(user_id, id_recomendacion, realizada):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False, "Error de conexión a la base de datos"

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)

            check_query = """
                SELECT ID_SEGUIMIENTO
                FROM TB_SEGUIMIENTO_RECOMENDACIONES
                WHERE ID_USUARIO = %s AND ID_RECOMENDACION = %s
                LIMIT 1
            """
            cursor.execute(check_query, (user_id, id_recomendacion))
            existing = cursor.fetchone()

            if existing:
                update_query = """
                    UPDATE TB_SEGUIMIENTO_RECOMENDACIONES
                    SET REALIZADA = %s,
                        FECHA_REGISTRO = NOW()
                    WHERE ID_SEGUIMIENTO = %s
                """
                cursor.execute(update_query, (realizada, existing["ID_SEGUIMIENTO"]))
            else:
                insert_query = """
                    INSERT INTO TB_SEGUIMIENTO_RECOMENDACIONES
                    (
                        ID_RECOMENDACION,
                        ID_USUARIO,
                        REALIZADA,
                        FECHA_REGISTRO
                    )
                    VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (id_recomendacion, user_id, realizada))

            connection.commit()
            return True, "Seguimiento guardado correctamente."

        except Exception as e:
            connection.rollback()
            print(f"Error al guardar seguimiento: {e}")
            return False, str(e)

        finally:
            if cursor:
                cursor.close()
            DatabaseConnection.close_connection(connection)