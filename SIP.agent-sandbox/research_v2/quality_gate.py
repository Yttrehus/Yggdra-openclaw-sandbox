import re
import os
import json

class ResearchQualityGate:
    """
    Implementerer kvalitetskontrol for research-filer (APA 7th + Epistemisk sporbarhed).
    """
    def __init__(self):
        self.rules = [
            {"id": "APA-001", "name": "Referenceliste", "pattern": r"(?i)#+ (Referencer|Kilder|Bibliography)"},
            {"id": "APA-002", "name": "Inline Citater", "pattern": r"\(\w+ et al\., \d{4}\)|\(\w+, \d{4}\)"},
            {"id": "STR-001", "name": "Metadata Sektion", "pattern": r"(?i)#+ Metadata|---\n(.*\n)*---"},
            {"id": "STR-002", "name": "Konklusion/Indsigt", "pattern": r"(?i)#+ (Konklusion|Indsigt|Nøgleindsigter|Takeaways)"}
        ]

    def audit_file(self, content):
        results = []
        score = 0
        for rule in self.rules:
            # Vi bruger re.search til at se om mønstret findes et sted i indholdet
            passed = bool(re.search(rule["pattern"], content))
            if passed: score += 1
            results.append({
                "id": rule["id"],
                "name": rule["name"],
                "passed": passed
            })

        quality_pct = (score / len(self.rules)) * 100
        
        return {
            "quality_score": quality_pct,
            "rules": results,
            "status": "PASS" if quality_pct >= 75 else "FAIL"
        }

    def audit_directory(self, directory_path):
        if not os.path.isdir(directory_path):
            return {"status": "ERROR", "error": f"Directory not found: {directory_path}"}

        audit_reports = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".md") and file != "README.md" and file != "INDEX.md":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    report = self.audit_file(content)
                    report["file"] = os.path.relpath(file_path, directory_path)
                    audit_reports.append(report)
        
        return audit_reports

if __name__ == "__main__":
    gate = ResearchQualityGate()
    
    # 1. Test på en enkelt fil (hvis den findes)
    landskab_dir = "2_research/llm-landskab"
    if os.path.isdir(landskab_dir):
        print(f"--- Auditing directory: {landskab_dir} ---")
        reports = gate.audit_directory(landskab_dir)
        
        passed_count = sum(1 for r in reports if r["status"] == "PASS")
        print(f"Files audited: {len(reports)}")
        print(f"Passed Quality Gate: {passed_count}")
        
        # Vis fejlede filer
        if passed_count < len(reports):
            print("\nFailed files:")
            for r in reports:
                if r["status"] == "FAIL":
                    failed_rules = [rule["name"] for rule in r["rules"] if not rule["passed"]]
                    print(f"  - {r['file']} (Score: {r['quality_score']}%). Missing: {', '.join(failed_rules)}")
