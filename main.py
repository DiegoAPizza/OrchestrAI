from graph.pipeline import pipeline
from domain.core.logging_config import setup_logging
import uuid
import time
from graph.pipeline import run_with_cache
if __name__ == "__main__":
    # Configurar logging
    logger = setup_logging()
    start = time.time()
    # thread_id identifica esta ejecución del pipeline
    config = {"configurable": {"thread_id": "run-001"}}
    run_with_cache("La inteligencia artificial en la medicina", "run-001")
    
    start = time.time()
    run_with_cache("IA aplicada a la salud y medicina", "run-002")
    print(f"Segunda vez: {time.time() - start:.1f}s")
    
   
    
    # Verificar que el checkpoint se guardó
    # Retomar desde el checkpoint con el mismo thread_id
   