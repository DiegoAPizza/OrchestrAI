from langchain_ollama import OllamaLLM
from pydantic import BaseModel

llm = OllamaLLM(model="llama3.2")

class EvalResult(BaseModel):
    eval_id: str
    topic: str
    relevancia: float
    precision: float
    estructura: float
    fluidez: float
    score_total: float
    passed: bool
    feedback: str

def judge_report(eval_id: str, topic: str, report: str, min_score: float) -> EvalResult:
    prompt = f"""You are an expert evaluator. Score this report on a scale of 1-10 for each criteria.

Topic requested: {topic}

Report to evaluate:
{report}

Evaluate and respond in this EXACT format (numbers only after the colon):
relevancia: [1-10]
precision: [1-10]
estructura: [1-10]
fluidez: [1-10]
feedback: [one sentence explanation]"""

    try:
        response = llm.invoke(prompt)
        print(f"DEBUG judge response:\n{response}") 
        # parsear la respuesta del judge
        relevancia = 0.0
        precision = 0.0
        estructura = 0.0
        fluidez = 0.0
        feedback = "No feedback provided"

        lista_scores = response.splitlines()
       
        for line in lista_scores:
            if line.startswith("relevancia:"):
                relevancia = float(line.split(":")[1].strip())
            elif line.startswith("precision:"):
                precision = float(line.split(":")[1].strip())
            elif line.startswith("estructura:"):
                estructura = float(line.split(":")[1].strip())
            elif line.startswith("fluidez:"):
                fluidez = float(line.split(":")[1].strip())
            elif line.startswith("feedback:"):
                feedback = line.split(":")[1].strip()
        # calcular promedio
        promedio=(relevancia + precision + estructura + fluidez) / 4
        passed = promedio >= min_score
        # retornar EvalResult
        return EvalResult(
            eval_id=eval_id,
            topic=topic,
            relevancia=relevancia,
            precision=precision,
            estructura=estructura,
            fluidez=fluidez,
            score_total=promedio,
            passed=passed,
            feedback=feedback
        )
    except Exception as e:
        # retornar EvalResult con score 0 y error en feedback
        return EvalResult(
            eval_id=eval_id,
            topic=topic,
            relevancia=0.0,
            precision=0.0,
            estructura=0.0,
            fluidez=0.0,
            score_total=0.0,
            passed=False,
            feedback=f"Error occurred while evaluating report: {str(e)}"
        )