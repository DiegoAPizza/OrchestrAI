import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from domain.state import PipelineState
from domain.agents.researcher import researcher_node
from domain.agents.analyst import analyst_node
from domain.agents.writer import writer_node
from domain.core.semantic_cache import SemanticCache
import uuid
cache= SemanticCache()

def should_continue(state: PipelineState) -> str:
    if state.get("errors"):
        return "end"
    return "continue"

def build_pipeline():
    # 1. Crear la conexión a SQLite (check_same_thread=False es necesario para LangGraph)
    conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
    
    # 2. Instanciar el checkpointer pasándole la conexión
    checkpointer = SqliteSaver(conn)
    
    graph = StateGraph(PipelineState)
    
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    
    graph.set_entry_point("researcher")
    
    graph.add_conditional_edges(
        "researcher",
        should_continue,
        {"continue": "analyst", "end": END}
    )
    graph.add_conditional_edges(
        "analyst",
        should_continue,
        {"continue": "writer", "end": END}
    )
    graph.add_edge("writer", END)
    
    # 3. Compilar con el checkpointer
    return graph.compile(checkpointer=checkpointer)

# Exportar la instancia global para que main.py la use
pipeline = build_pipeline()

def run_with_cache(topic: str, thread_id: str) -> dict:
    # 1. Buscar en cache
    cached = cache.get(topic)
    if cached:
        print(f"🎯 Cache HIT para: '{topic}'")
        return cached
    
    print(f"⚡ Cache MISS — corriendo pipeline para: '{topic}'")
    
    # 2. Correr pipeline
    config = {"configurable": {"thread_id": thread_id}}
    result = pipeline.invoke(
        {
            "topic": topic,
            "research_results": None,
            "analysis": None,
            "final_report": None,
            "current_step": "start",
            "errors": [],
            "trace_id": str(uuid.uuid4())
        },
        config=config
    )
    
    # 3. Guardar en cache
    cache.set(topic, result)
    return result