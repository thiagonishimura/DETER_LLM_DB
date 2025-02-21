import os
import psycopg2
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
def connect_to_db():
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_DB_HOST"),
        port=os.getenv("POSTGRES_DB_PORT"),
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_DB_USER"),
        password=os.getenv("POSTGRES_DB_PASSWORD")
    )
    return connection

# Extração do esquema de múltiplos schemas
def extract_db_schema(schemas):
    connection = connect_to_db()
    cursor = connection.cursor()

    schema_info = {}

    for schema in schemas:
        schema_query = f"""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
            ORDER BY table_name, ordinal_position;
        """

        cursor.execute(schema_query)
        results = cursor.fetchall()

        for table, column, data_type in results:
            schema_key = f"{schema}.{table}"  # Inclui o nome do schema
            if schema_key not in schema_info:
                schema_info[schema_key] = []
            schema_info[schema_key].append((column, data_type))

    cursor.close()
    connection.close()

    return schema_info

# Exibir o esquema extraído
def display_schema():
    schemas = ['public', 'terraamazon', 'terrabrasilis']
    schema = extract_db_schema(schemas)
    for table, columns in schema.items():
        print(f"Schema e Tabela: {table}")
        for column, data_type in columns:
            print(f"  - {column}: {data_type}")
        print("\n")

# Salvar esquema em arquivo JSON
def save_schema_to_file():
    schemas = ['public', 'terraamazon', 'terrabrasilis']
    schema = extract_db_schema(schemas)
    with open("memory/db_schema.json", "w") as file:
        json.dump(schema, file, indent=4)