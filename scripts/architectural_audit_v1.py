#!/usr/bin/env python3
"""
Yggdra Architectural Audit v1.0
Fokus: Identifikation af teknisk gæld, redundante moduler og optimerings-potentiale efter V1-V20 roadmappets fuldførelse.
"""
import os
import json
from datetime import datetime

class ArchitecturalAudit:
    def __init__(self, scripts_dir="scripts"):
        self.scripts_dir = scripts_dir
        self.report_path = "research/reports/architectural_audit_report.json"

    def perform_audit(self):
        print("--- Yggdra Architectural Audit v1.0 ---")
        files = [f for f in os.listdir(self.scripts_dir) if f.endswith('.py')]
        print(f"[PROCESS]: Skanner {len(files)} scripts for redundans...")

        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(files),
            "categories": {
                "core": [],
                "mock_demo": [],
                "v_series": [],
                "utility": []
            },
            "redundancy_candidates": []
        }

        for file in files:
            if file.startswith('v') and any(char.isdigit() for char in file):
                audit_results["categories"]["v_series"].append(file)
                if "demo" in file or "test" in file:
                    audit_results["redundancy_candidates"].append(file)
            elif "mock" in file:
                audit_results["categories"]["mock_demo"].append(file)
                audit_results["redundancy_candidates"].append(file)
            elif file in ["get_context.py", "memory.py", "notion_sync.py", "vidar_security_scan.py"]:
                audit_results["categories"]["core"].append(file)
            else:
                audit_results["categories"]["utility"].append(file)

        print(f"[SUCCESS]: Audit færdig. Fundet {len(audit_results['redundancy_candidates'])} kandidater til arkivering.")
        
        # Gem rapport
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        with open(self.report_path, "w") as f:
            json.dump(audit_results, f, indent=2)
        
        return audit_results

if __name__ == "__main__":
    audit = ArchitecturalAudit()
    audit.perform_audit()
