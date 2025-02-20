import os
import psycopg2
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados
DB_HOST = os.getenv("POSTGRES_DB_HOST")
DB_PORT = os.getenv("POSTGRES_DB_PORT")
DB_NAME = os.getenv("POSTGRES_DB_NAME")
DB_USER = os.getenv("POSTGRES_DB_USER")
DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD")

def get_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None
