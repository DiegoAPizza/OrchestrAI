from graph.pipeline import pipeline
from evals.dataset import EVAL_DATASET
from evals.judge import judge_report, EvalResult
from typing import List


def run_evals() -> List[EvalResult]:
    results = []
    
    for case in EVAL_DATASET:
        print(f"\nRunning eval: {case['id']} — {case['topic']}")
        
        # 1. Correr el pipeline
        config = {"configurable": {"thread_id": case["id"]}}
        state = pipeline.invoke(
            {
                "topic": case["topic"],
                "research_results": None,
                "analysis": None,
                "final_report": None,
                "current_step": "start",
                "errors": []
            },
            config=config
        )
        
        # 2. Verificar que el pipeline no tuvo errores
        if state["errors"]:
            print(f"  Pipeline error: {state['errors']}")
            continue
        
        # 3. Evaluar con el judge
        result = judge_report(
            eval_id=case["id"],
            topic=case["topic"],
            report=state["final_report"],
            min_score=case["min_score"]
        )
        
        # 4. Verificar keywords
        report_lower = state["final_report"].lower()
        keywords_found = [k for k in case["expected_keywords"] if k in report_lower]
        keywords_missing = [k for k in case["expected_keywords"] if k not in report_lower]
        
        print(f"  Score: {result.score_total:.1f}/10 — {'✅ PASSED' if result.passed else '❌ FAILED'}")
        print(f"  Keywords found: {keywords_found}")
        print(f"  Keywords missing: {keywords_missing}")
        print(f"  Feedback: {result.feedback}")
        
        results.append(result)
    
    # 5. Resumen final
    passed = sum(1 for r in results if r.passed)
    print(f"\n=== EVAL SUMMARY ===")
    print(f"Passed: {passed}/{len(results)}")
    print(f"Average score: {sum(r.score_total for r in results) / len(results):.1f}/10")
    
    return results


if __name__ == "__main__":
    run_evals()