import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Mock config baseret på PIPELINE_DESIGN.md
PIPELINE_EXPECTATIONS = {
    "ai_intelligence": {
        "output_pattern": "data/intelligence/daily_{date}.md",
        "max_age_hours": 28,
        "description": "Indsamler nyheder fra RSS, HN, Twitter osv."
    },
    "youtube_monitor": {
        "output_pattern": "data/intelligence/yt_daily_{date}.md",
        "max_age_hours": 28,
        "description": "Overvåger YouTube kanaler for nye videoer."
    },
    "fact_extraction": {
        "output_pattern": "data/extracted_facts.json",
        "max_age_hours": 48,
        "description": "Ekstraherer fakta fra chatlogs."
    }
}

def check_pipeline_health(workspace_root="."):
    """Verificér at alle pipelines har produceret output inden for forventet tidsramme."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    findings = []
    
    print(f"--- Pipeline Health Check at {now.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    for name, cfg in PIPELINE_EXPECTATIONS.items():
        pattern = cfg["output_pattern"]
        
        # Check for i dag
        expected_path = Path(workspace_root) / pattern.format(date=today_str)
        
        # Hvis den ikke findes for i dag, check i går
        if not expected_path.exists():
            expected_path = Path(workspace_root) / pattern.format(date=yesterday_str)
            
        # Speciel case for statiske filer uden dato i navnet
        if "{date}" not in pattern:
            expected_path = Path(workspace_root) / pattern
            
        status = "OK"
        age_str = "N/A"
        
        if expected_path.exists():
            mtime = datetime.fromtimestamp(expected_path.stat().st_mtime)
            age_hours = (now - mtime).total_seconds() / 3600
            age_str = f"{age_hours:.1f}h"
            
            if age_hours > cfg["max_age_hours"]:
                status = "STALE"
                findings.append(f"ALERT: {name} er forældet ({age_str} > {cfg['max_age_hours']}h)")
        else:
            status = "MISSING"
            findings.append(f"ALERT: {name} har ikke produceret output (tjekkede i dag/i går)")
            
        print(f"[{status:<7}] {name:<15} | Age: {age_str:<6} | Expects: <{cfg['max_age_hours']}h")

    if not findings:
        print("\nAll pipelines healthy.")
    else:
        print("\nHealth Issues Found:")
        for issue in findings:
            print(f"- {issue}")
            
    return findings

if __name__ == "__main__":
    # Simuler check i sandkassen
    # Vi opretter nogle dummy filer for at teste logikken
    test_root = Path("SIP.agent-sandbox/pipeline_v2/test_root")
    data_dir = test_root / "data/intelligence"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 1. ai_intelligence: i går (OK)
    (data_dir / f"daily_{yesterday}.md").write_text("Test content")
    
    # 2. youtube_monitor: i dag (OK)
    (data_dir / f"yt_daily_{today}.md").write_text("Test content")
    
    # 3. fact_extraction: statisk fil (MISSING)
    # (data_dir / "extracted_facts.json").write_text("{}")
    
    # Kør checket mod test-root
    check_pipeline_health(workspace_root="SIP.agent-sandbox/pipeline_v2/test_root")
