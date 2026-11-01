from graph.pipeline import pipeline

if __name__ == "__main__":
    result = pipeline.invoke({
        "topic": "La inteligencia artificial en la medicina",
        "research_results": None,
        "analysis": None,
        "final_report": None,
        "current_step": "start",
        "errors": []
    })
    
    print("=== REPORTE FINAL ===")
    print(result["final_report"])
    print(f"\nÚltimo paso: {result['current_step']}")
    print(f"Errores: {result['errors']}")