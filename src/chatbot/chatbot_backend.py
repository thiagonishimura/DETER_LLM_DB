# from typing import List, Tuple
# from chatbot.load_config import LoadProjectConfig
# from agent_graph.load_tools_config import LoadToolsConfig
# from agent_graph.build_full_graph import build_graph
# from utils.app_utils import create_directory
# from chatbot.memory import Memory

# URL = "https://github.com/Farzad-R/LLM-Zero-to-Hundred/tree/master/RAG-GPT"
# hyperlink = f"[RAG-GPT user guideline]({URL})"

# PROJECT_CFG = LoadProjectConfig()
# TOOLS_CFG = LoadToolsConfig()

# graph = build_graph()
# config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}

# create_directory("memory")


# class ChatBot:

#     @staticmethod
#     def respond(chatbot: List, message: str) -> Tuple:
#         try:
#             events = graph.stream(
#                 {"messages": [("user", message)]}, config, stream_mode="values"
#             )

#             for event in events:
#                 # Log para depurar event completo
#                 print("Event recebido:", event)

#                 event["messages"][-1].pretty_print()

#             chatbot.append(
#                 (message, event["messages"][-1].content)
#             )

#         except Exception as e:
#             error_message = f"Ocorreu um erro durante o processamento: {str(e)}. Tente novamente."
#             chatbot.append((message, error_message))
#             print("Erro detalhado:", e)  # Log do erro completo

#         Memory.write_chat_history_to_file(
#             gradio_chatbot=chatbot, folder_path=PROJECT_CFG.memory_dir, thread_id=TOOLS_CFG.thread_id
#         )
#         return "", chatbot

from typing import List, Tuple
from chatbot.load_config import LoadProjectConfig
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.build_full_graph import build_graph
from utils.app_utils import create_directory
from chatbot.memory import Memory
from agent_graph.table_mapping import TABLE_MAPPING

PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()
graph = build_graph()
config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}
create_directory("memory")

import psycopg2

class ChatBot:

    @staticmethod
    def respond(chatbot: List, message: str) -> Tuple:
        try:
            # Detectar automaticamente a tabela, schema e coluna com base no mapeamento
            detected_schema = None
            detected_table = None
            detected_column = None

            for keyword, table_info in TABLE_MAPPING.items():
                if keyword.lower() in message.lower():
                    detected_schema = table_info["Schemas"]
                    detected_table = table_info["Tables"]
                    detected_column = table_info["Columns"]
                    break

            # Verifique se encontrou um mapeamento para tabela/coluna
            if detected_schema and detected_table and detected_column:
                # Query SQL formatada com schema, tabela e coluna
                query = f"SELECT {detected_column} FROM {detected_schema}.{detected_table}"
                print(f"Executando query: {query}")

                # Conectar ao banco de dados
                connection = psycopg2.connect(
                    host="localhost", database="amazonia", user="postgres", password="postgres"
                )
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                connection.close()

                # Processar e retornar o resultado
                chatbot.append((message, str(result)))

            else:
                chatbot.append((message, "Não encontrei uma tabela correspondente para a consulta."))
            
        except Exception as e:
            error_message = f"Ocorreu um erro durante o processamento: {str(e)}. Tente novamente."
            chatbot.append((message, error_message))
            print("Erro detalhado:", e)

        Memory.write_chat_history_to_file(
            gradio_chatbot=chatbot, folder_path=PROJECT_CFG.memory_dir, thread_id=TOOLS_CFG.thread_id
        )
        return "", chatbot
