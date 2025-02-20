import os
import psycopg2
from psycopg2 import OperationalError

class TestPostgresConnection:
    def __init__(self):
        self.db_name = os.getenv("POSTGRES_DB_NAME")
        self.db_user = os.getenv("POSTGRES_DB_USER")
        self.db_password = os.getenv("POSTGRES_DB_PASSWORD")
        self.db_host = os.getenv("POSTGRES_DB_HOST")
        self.db_port = os.getenv("POSTGRES_DB_PORT")

    def test_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            print("Conexão bem-sucedida ao banco de dados!")
            conn.close()
        except OperationalError as e:
            print(f"Erro na conexão: {e}")

# Instanciando a classe e testando a conexão
test_connection = TestPostgresConnection()
test_connection.test_connection()
