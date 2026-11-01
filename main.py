from graph.pipeline import pipeline

if __name__ == "__main__":
    # thread_id identifica esta ejecución del pipeline
    config = {"configurable": {"thread_id": "run-001"}}
    
    result = pipeline.invoke(
        {
            "topic": "La inteligencia artificial en la medicina",
            "research_results": None,
            "analysis": None,
            "final_report": None,
            "current_step": "start",
            "errors": []
        },
        config=config
    )
    
    print("=== REPORTE FINAL ===")
    print(result["final_report"])
    print(f"\nÚltimo paso: {result['current_step']}")
    
    # Verificar que el checkpoint se guardó
    # Retomar desde el checkpoint con el mismo thread_id
    print("\n=== RETOMANDO DESDE CHECKPOINT ===")
    state = pipeline.get_state(config)
    print(f"Paso guardado: {state.values['current_step']}")