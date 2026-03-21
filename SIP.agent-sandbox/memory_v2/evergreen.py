import json
import os
from datetime import datetime, timezone

class EvergreenManager:
    """
    Håndterer identifikation af 'evergreen' indhold, 
    der ikke skal decayes (Fase 1 udvidelse).
    """
    
    # Mapper og filtyper der som standard er evergreen
    EVERGREEN_PATHS = [
        "manuals/",
        "KNB.manuals/",
        "REF.",
        "BLUEPRINT.md",
        "IDENTITY.md"
    ]
    
    # Kategorier af fakta der er evergreen
    EVERGREEN_CATEGORIES = [
        "established",
        "core_principle",
        "meta"
    ]

    def is_evergreen(self, point_payload):
        """
        Afgør om et Qdrant point er evergreen baseret på payload.
        """
        source_path = point_payload.get("source_path", "")
        category = point_payload.get("confidence", "") or point_payload.get("category", "")
        
        # 1. Tjek stier
        for path in self.EVERGREEN_PATHS:
            if path in source_path:
                return True
        
        # 2. Tjek kategorier
        if category in self.EVERGREEN_CATEGORIES:
            return True
            
        # 3. Tjek for eksplicit tag
        if point_payload.get("is_evergreen") is True:
            return True
            
        return False

    def get_decay_factor(self, point_payload, default_decay_factor):
        """
        Returnerer 1.0 hvis evergreen, ellers den beregnede decay factor.
        """
        if self.is_evergreen(point_payload):
            return 1.0
        return default_decay_factor

if __name__ == "__main__":
    manager = EvergreenManager()
    
    test_cases = [
        {"source_path": "manuals/git.md", "category": "info", "expected": True},
        {"source_path": "SIP.agent-sandbox/test.md", "category": "action", "expected": False},
        {"source_path": "BMS.auto-chatlog/logs.json", "category": "meta", "expected": True},
    ]
    
    print("--- Evergreen Manager Test ---")
    for tc in test_cases:
        res = manager.is_evergreen(tc)
        print(f"Path: {tc['source_path']:<30} | Evergreen: {res} (Expected: {tc['expected']})")
