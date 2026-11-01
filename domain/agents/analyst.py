from langchain_ollama import OllamaLLM
from domain.state import PipelineState

llm = OllamaLLM(model="llama3.2")

def analyst_node(state: PipelineState) -> dict:
    research_results = state["research_results"]
    
    prompt =  f"""You are an analyst agent.
    Given the following research, provide a critical analysis:
    - Identify patterns and insights
    - Highlight the most important findings
    - Structure the information clearly

    Research to analyze:
    {research_results}

    Critical Analysis:"""
    
    try:
        result = llm.invoke(prompt)
        return {
            "analysis": result,
            "current_step": "analyst_done"
        }
    except Exception as e:
        return {
            "errors": state.get("errors", []) + [f"Analyst error: {str(e)}"],
            "current_step": "analyst_failed"
        }