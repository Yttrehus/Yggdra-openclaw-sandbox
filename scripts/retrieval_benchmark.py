#!/usr/bin/env python3
"""
Retrieval Benchmark v1.0
Måler præcision og recall for Yggdras Retrieval Engine.
Bruger dataset.json som ground truth.
"""

import os
import sys
import json
from datetime import datetime

# Setup paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
sys.path.append(_SCRIPT_DIR)

DATASET_PATH = os.path.join(_PROJECT_ROOT, "SIP.agent-sandbox/retrieval_eval/dataset.json")

def run_benchmark():
    print("--- Yggdra Retrieval Benchmark v1.0 ---")
    
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return

    with open(DATASET_PATH, 'r') as f:
        dataset = json.load(f)

    # Importer søgemotoren
    try:
        from get_context import search_hybrid
    except ImportError:
        print("Error: Could not import search_hybrid from get_context.py")
        return

    results = []
    
    for case in dataset['test_cases']:
        query = case['query']
        target = case['target_collection']
        ground_truth = case['ground_truth_snippets']
        
        print(f"Testing TC: {case['id']} ('{query}') on collection '{target}'...")
        
        try:
            # Vi udfører den reelle søgning
            points = search_hybrid(query, target, limit=5)
            
            hits = 0
            for snippet in ground_truth:
                for p in points:
                    payload_str = str(p.payload).lower()
                    if snippet.lower() in payload_str:
                        hits += 1
                        break
            
            precision = hits / len(points) if points else 0
            recall = hits / len(ground_truth) if ground_truth else 0
            
            results.append({
                "id": case['id'],
                "precision": precision,
                "recall": recall
            })
            print(f"  Result: Precision={precision:.2f}, Recall={recall:.2f}")
            
        except Exception as e:
            print(f"  Search failed: {e}")

    if results:
        avg_p = sum(r['precision'] for r in results) / len(results)
        avg_r = sum(r['recall'] for r in results) / len(results)
        
        print("\n--- BENCHMARK SUMMARY ---")
        print(f"Total Cases: {len(results)}")
        print(f"Avg Precision: {avg_p:.2f}")
        print(f"Avg Recall: {avg_r:.2f}")
        
        # Gem resultat
        report_path = os.path.join(_PROJECT_ROOT, "data/retrieval_benchmark_latest.json")
        with open(report_path, 'w') as f:
            json.dump({"date": datetime.now().isoformat(), "summary": {"precision": avg_p, "recall": avg_r}, "details": results}, f, indent=2)
        print(f"\nReport saved to data/retrieval_benchmark_latest.json")

if __name__ == "__main__":
    run_benchmark()
