import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

load_dotenv()

print(f"POSTGRES_DB_HOST: {os.getenv('POSTGRES_DB_HOST')}")
print(f"POSTGRES_DB_PORT: {os.getenv('POSTGRES_DB_PORT')}")
print(f"POSTGRES_DB_NAME: {os.getenv('POSTGRES_DB_NAME')}")
print(f"POSTGRES_DB_USER: {os.getenv('POSTGRES_DB_USER')}")
print(f"POSTGRES_DB_PASSWORD: {os.getenv('POSTGRES_DB_PASSWORD')}")

class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("configs/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Definir variáveis ​​de ambiente
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")

        # Agente primário
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Configuração de pesquisa na Internet
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])

        # Configurações RAG auto_pdi_deter
        self.auto_pdi_deter_rag_llm = app_config["auto_pdi_deter_rag"]["llm"]
        self.auto_pdi_deter_rag_llm_temperature = float(
            app_config["auto_pdi_deter_rag"]["llm_temperature"])
        self.auto_pdi_deter_rag_embedding_model = app_config["auto_pdi_deter_rag"]["embedding_model"]
        self.auto_pdi_deter_rag_vectordb_directory = str(here(
            app_config["auto_pdi_deter_rag"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.auto_pdi_deter_unstructured_docs_directory = str(here(
            app_config["auto_pdi_deter_rag"]["unstructured_docs"]))
        self.auto_pdi_deter_rag_k = app_config["auto_pdi_deter_rag"]["k"]
        self.auto_pdi_deter_rag_chunk_size = app_config["auto_pdi_deter_rag"]["chunk_size"]
        self.auto_pdi_deter_rag_chunk_overlap = app_config["auto_pdi_deter_rag"]["chunk_overlap"]
        self.auto_pdi_deter_rag_collection_name = app_config["auto_pdi_deter_rag"]["collection_name"]

        # Configurações Chinook SQL agent
        self.chinook_sqldb_directory = str(here(
            app_config["chinook_sqlagent_configs"]["chinook_sqldb_dir"]))
        self.chinook_sqlagent_llm = app_config["chinook_sqlagent_configs"]["llm"]
        self.chinook_sqlagent_llm_temperature = float(
            app_config["chinook_sqlagent_configs"]["llm_temperature"])
        
        # Configurações PostgreSQL agent
        self.postgres_db_host = os.getenv("POSTGRES_DB_HOST", app_config["postgres_sqlagent_configs"]["db_host"])
        self.postgres_db_port = os.getenv("POSTGRES_DB_PORT", app_config["postgres_sqlagent_configs"]["db_port"])
        self.postgres_db_name = os.getenv("POSTGRES_DB_NAME", app_config["postgres_sqlagent_configs"]["db_name"])
        self.postgres_db_user = os.getenv("POSTGRES_DB_USER", app_config["postgres_sqlagent_configs"]["db_user"])
        self.postgres_db_password = os.getenv("POSTGRES_DB_PASSWORD", app_config["postgres_sqlagent_configs"]["db_password"])

        self.postgres_sqlagent_llm = app_config["postgres_sqlagent_configs"]["llm"]
        self.postgres_sqlagent_llm_temperature = float(app_config["postgres_sqlagent_configs"]["llm_temperature"])


        # Configurações Graph
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])
