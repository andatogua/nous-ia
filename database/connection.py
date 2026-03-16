import mysql.connector
from mysql.connector import Error
from config.settings import Settings


class DatabaseConnection:

    @staticmethod
    def get_connection():

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
            print(f"MySQL connection error: {e}")
            return None


    @staticmethod
    def close_connection(connection):

        if connection and connection.is_connected():
            connection.close()