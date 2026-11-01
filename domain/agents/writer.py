from langchain_ollama import OllamaLLM
from domain.state import PipelineState

llm = OllamaLLM(model="llama3.2")

def writer_node(state: PipelineState) -> dict:
    analist_result = state["analysis"]
    research_results = state["research_results"]
    prompt = f"""You are an expert content writer and storyteller. 
    Your task is to synthesize the provided research and critical analysis into a highly readable, engaging, and well-structured article.

    Guidelines:
    - Write a compelling introduction that hooks the reader.
    - Organize the information into logical, well-flowing paragraphs (avoid just listing bullet points).
    - Use a professional yet accessible tone, avoiding unnecessary jargon.
    - Seamlessly integrate the key insights from the analysis into the narrative.
    - Finish with a strong conclusion that summarizes the main takeaway.

    Original Research:
    {research_results}

    Critical Analysis:
    {analist_result}

    Final Article:"""
    
    try:
        result = llm.invoke(prompt)
        return {
            "final_report": result,
            "current_step": "writing_done"
        }
    except Exception as e:
        return {
            "errors": state.get("errors", []) + [f"Writer error: {str(e)}"],
            "current_step": "writer_failed"
        }