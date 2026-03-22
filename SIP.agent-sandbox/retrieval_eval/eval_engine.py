import json
import os
import sys
from datetime import datetime

class RetrievalEvaluator:
    def __init__(self, dataset_path):
        with open(dataset_path, 'r') as f:
            self.dataset = json.load(f)
        self.results = []

    def evaluate_case(self, test_case, retrieved_points):
        """
        Beregner metrics for et enkelt test case.
        retrieved_points er en liste af payloads/tekster.
        """
        ground_truth = test_case['ground_truth_snippets']
        hits = 0
        hit_details = []
        
        for snippet in ground_truth:
            found = False
            for point in retrieved_points:
                # Konvertér point til tekst hvis det er et objekt
                point_text = json.dumps(point) if isinstance(point, (dict, list)) else str(point)
                if snippet.lower() in point_text.lower():
                    hits += 1
                    found = True
                    break
            hit_details.append({"snippet": snippet, "found": found})
            
        precision = hits / len(retrieved_points) if retrieved_points else 0
        recall = hits / len(ground_truth) if ground_truth else 0
        
        return {
            "test_id": test_case['id'],
            "query": test_case['query'],
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "hit_details": hit_details
        }

    def run_benchmark(self, retrieval_function):
        """
        Kører benchmark mod en given retrieval-funktion.
        retrieval_function skal tage (query, collection, limit) og returnere points.
        """
        benchmark_results = []
        for tc in self.dataset['test_cases']:
            print(f"Evaluerer {tc['id']}: '{tc['query']}'...")
            try:
                points = retrieval_function(tc['query'], tc['target_collection'], limit=5)
                res = self.evaluate_case(tc, points)
                benchmark_results.append(res)
            except Exception as e:
                print(f"  FEJL under evaluering af {tc['id']}: {e}")
            
        summary = self.calculate_summary(benchmark_results)
        return {"results": benchmark_results, "summary": summary}

    def calculate_summary(self, results):
        if not results:
            return {"avg_precision": 0, "avg_recall": 0, "total_cases": 0}
        avg_p = sum(r['precision'] for r in results) / len(results)
        avg_r = sum(r['recall'] for r in results) / len(results)
        return {
            "avg_precision": round(avg_p, 3),
            "avg_recall": round(avg_r, 3),
            "total_cases": len(results)
        }

# --- Mock Implementation for demonstration ---
def mock_retrieval(query, collection, limit=5):
    # Simuleret succesfuld retrieval for demonstration
    if "McDonalds" in query:
        return [{"text": "McDonalds ligger på Marsvej 2, 8960 Randers SØ"}]
    if "vision" in query:
        return [{"text": "Yggdra er et personligt kognitivt exoskeleton"}]
    return []

if __name__ == "__main__":
    dataset_file = "SIP.agent-sandbox/retrieval_eval/dataset.json"
    if not os.path.exists(dataset_file):
        print(f"Fejl: Fandt ikke dataset på {dataset_file}")
        sys.exit(1)
        
    evaluator = RetrievalEvaluator(dataset_file)
    print("--- Starter Yggdra Retrieval Benchmark (Demo Mode) ---")
    report = evaluator.run_benchmark(mock_retrieval)
    print("\nBenchmark Rapport:")
    print(json.dumps(report['summary'], indent=2))
