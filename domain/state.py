from typing import TypedDict, Optional, List

class PipelineState(TypedDict):
    topic: str                          # el tema pedido por el usuario
    research_results: Optional[str]     # output del Investigador
    analysis: Optional[str]             # output del Analista
    final_report: Optional[str]         # output del Escritor
    current_step: str                   # en qué paso está el pipeline
    errors: List[str]                   # errores acumulados
    trace_id:str                        # ID de rastreo para el pipeline