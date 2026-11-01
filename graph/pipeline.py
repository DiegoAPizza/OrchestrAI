from langgraph.graph import StateGraph, END
from domain.state import PipelineState
from domain.agents.researcher import researcher_node
from domain.agents.analyst import analyst_node
from domain.agents.writer import writer_node


def should_continue(state: PipelineState) -> str:
    """Edge condicional — si hay error, termina el pipeline."""
    if state.get("errors"):
        return "end"
    return "continue"


def build_pipeline():
    graph = StateGraph(PipelineState)
    
    # Registrar nodos
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    
    # Punto de entrada
    graph.set_entry_point("researcher")
    
    # Edges condicionales
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
    
    # Edge fijo — writer siempre termina
    graph.add_edge("writer", END)
    
    return graph.compile()


pipeline = build_pipeline()