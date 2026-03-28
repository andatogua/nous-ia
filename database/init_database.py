import os
import mysql.connector
from mysql.connector import Error
from config.settings import Settings


class DatabaseInitializer:

    @staticmethod
    def _get_connection_without_database():
        try:
            connection = mysql.connector.connect(
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    @staticmethod
    def _get_connection_with_database():
        try:
            connection = mysql.connector.connect(
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD,
                database=Settings.DB_NAME
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    @staticmethod
    def _ensure_database_exists():
        connection = DatabaseInitializer._get_connection_without_database()
        if not connection:
            return False

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Settings.DB_NAME}")
            connection.commit()
            return True
        except Error as e:
            print(f"Error al crear la base de datos: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def _get_sql_script_path(filename="bd_salud_mental.sql"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        return os.path.join(project_root, "sql", filename)

    @staticmethod
    def _execute_sql_file(filepath):
        if not os.path.exists(filepath):
            print(f"Script SQL no encontrado: {filepath}")
            return False

        connection = DatabaseInitializer._get_connection_with_database()
        if not connection:
            return False

        cursor = None
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                sql_script = file.read()

            statements = []
            current_statement = []
            in_multiline_comment = False

            for line in sql_script.split('\n'):
                stripped = line.strip()

                if stripped.startswith('--'):
                    continue

                if '/*' in stripped:
                    in_multiline_comment = True
                if '*/' in stripped:
                    in_multiline_comment = False
                    continue

                if not in_multiline_comment and stripped:
                    current_statement.append(line)

                if not in_multiline_comment and stripped.endswith(';'):
                    statement = '\n'.join(current_statement)
                    if statement.strip():
                        statements.append(statement)
                    current_statement = []

            if current_statement:
                statement = '\n'.join(current_statement)
                if statement.strip():
                    statements.append(statement)

            cursor = connection.cursor()

            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        connection.commit()
                    except Error as e:
                        if 'Duplicate entry' not in str(e) and 'already exists' not in str(e):
                            print(f"Nota al ejecutar SQL: {e}")

            return True

        except Exception as e:
            print(f"Error al ejecutar script SQL: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @staticmethod
    def initialize():
        print("Inicializando base de datos...")

        if not DatabaseInitializer._ensure_database_exists():
            print("Error: No se pudo crear la base de datos")
            return False

        main_script = DatabaseInitializer._get_sql_script_path("bd_salud_mental.sql")
        if not DatabaseInitializer._execute_sql_file(main_script):
            print("Error: No se pudo ejecutar el script SQL principal")
            return False

        update_script = DatabaseInitializer._get_sql_script_path("tables_update.sql")
        DatabaseInitializer._execute_sql_file(update_script)

        print("Base de datos inicializada correctamente")
        return True
