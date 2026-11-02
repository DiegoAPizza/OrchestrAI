from typing import TypedDict, List

class EvalCase(TypedDict):
    id: str
    topic: str
    expected_keywords: List[str]  # palabras que deberían aparecer
    min_score: float              # score mínimo aceptable (0-10)

EVAL_DATASET: List[EvalCase] = [
     {
         "id": "eval-001",
         "topic": "La inteligencia artificial en la medicina",
         "expected_keywords": ["diagnóstico", "pacientes", "algoritmos"],
         "min_score": 7.0
    },
    {
        "id": "eval-002", 
        "topic": "El cambio climático y sus efectos",
        "expected_keywords": ["temperatura", "emisiones", "impacto"],
        "min_score": 7.0
    } ,
    {
        "id": "eval-003",
        "topic": "El futuro de la energía renovable",
        "expected_keywords": ["solar", "eólica", "sostenible"],
        "min_score": 7.0
    }
]