import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.tools import tool

load_dotenv()

class PostgresSQLAgent:
    def __init__(self, llm: str, llm_temperature: float) -> None:
        self.sql_agent_llm = ChatOpenAI(model=llm, temperature=llm_temperature)

        db_host = os.getenv("POSTGRES_DB_HOST")
        db_port = os.getenv("POSTGRES_DB_PORT")
        db_name = os.getenv("POSTGRES_DB_NAME")
        db_user = os.getenv("POSTGRES_DB_USER")
        db_password = os.getenv("POSTGRES_DB_PASSWORD")

        self.db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        self.db = SQLDatabase.from_uri(self.db_uri)

        self.full_chain = create_sql_query_chain(self.sql_agent_llm, self.db)

@tool
def query_postgres_sqldb(query: str) -> str:
    """Executa uma consulta SQL no banco de dados PostgreSQL e retorna os resultados."""
    agent = PostgresSQLAgent(
        llm="gpt-3.5-turbo",
        llm_temperature=0.5
    )
    query = agent.full_chain.invoke({"question": query})
    return agent.db.run(query)
