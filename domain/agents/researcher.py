from langchain_ollama import OllamaLLM
from domain.state import PipelineState

llm = OllamaLLM(model="llama3.2")

def researcher_node(state: PipelineState) -> dict:
    topic = state["topic"]
    
    prompt = f"""You are a research agent. 
Research the following topic and provide key facts and information.
Topic: {topic}

Provide a comprehensive research summary with:
- Key facts
- Important context
- Relevant data points

Research Summary:"""
    
    try:
        result = llm.invoke(prompt)
        return {
            "research_results": result,
            "current_step": "research_done"
        }
    except Exception as e:
        return {
            "errors": state.get("errors", []) + [f"Researcher error: {str(e)}"],
            "current_step": "research_failed"
        }