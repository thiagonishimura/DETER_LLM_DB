from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from agent_graph.tool_chinook_sqlagent import query_chinook_sqldb
from agent_graph.tool_tavily_search import load_tavily_search_tool
from agent_graph.tool_auto_pdi_deter_rag import auto_pdi_deter
from agent_graph.tool_postgres_sqlagent import query_postgres_sqldb
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.agent_backend import State, BasicToolNode, route_tools, plot_agent_schema
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


TOOLS_CFG = LoadToolsConfig()


def build_graph():

    primary_llm = ChatOpenAI(model=TOOLS_CFG.primary_agent_llm,
                             temperature=TOOLS_CFG.primary_agent_llm_temperature)
    graph_builder = StateGraph(State)

    search_tool = load_tavily_search_tool(TOOLS_CFG.tavily_search_max_results)
    tools = [
        search_tool,
        auto_pdi_deter,
        query_chinook_sqldb,
        query_postgres_sqldb,
        ]
    
    primary_llm_with_tools = primary_llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [primary_llm_with_tools.invoke(state["messages"])]}

    graph_builder.add_node("chatbot", chatbot)
    tool_node = BasicToolNode(
        tools=[
            search_tool,
            auto_pdi_deter,
            query_chinook_sqldb,
            query_postgres_sqldb,     
        ])
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,

        {"tools": "tools", "__end__": "__end__"},
    )

    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    plot_agent_schema(graph)
    return graph
