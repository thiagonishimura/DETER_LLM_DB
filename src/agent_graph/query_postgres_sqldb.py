import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from agent_graph.load_tools_config import LoadToolsConfig

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class PostgresDB:
    def __init__(self):
        config = LoadToolsConfig()
        self.conn = psycopg2.connect(
            dbname=config.postgres_db_name,
            user=config.postgres_db_user,
            password=config.postgres_db_password,
            host=config.postgres_db_host,
            port=config.postgres_db_port
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        """Executa uma query no banco e retorna os resultados."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close_connection(self):
        """Fecha a conexão com o banco."""
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db = PostgresDB()
    result = db.execute_query("SELECT version();")
    print(result)
    db.close_connection()
