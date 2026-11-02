from langchain_ollama import OllamaLLM
from domain.state import PipelineState
import logging
import time
import json

logger = logging.getLogger("agentcore.writer")
llm = OllamaLLM(model="llama3.2")

def writer_node(state: PipelineState) -> dict:
    trace_id = state["trace_id"]
    start = time.time()
    
    logger.info(json.dumps({
        "trace_id": trace_id,
        "node": "writer",
        "event": "started"
    }))
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
        elapsed = time.time() - start
        logger.info(json.dumps({
        "trace_id": trace_id,
        "node": "writer", 
        "event": "completed",
        "elapsed_seconds": round(elapsed, 2)
    }))
        return {
            "final_report": result,
            "current_step": "writing_done"
        }
    except Exception as e:
        return {
            "errors": state.get("errors", []) + [f"Writer error: {str(e)}"],
            "current_step": "writer_failed"
        }