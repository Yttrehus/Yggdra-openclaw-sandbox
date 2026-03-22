import os
import json

class EvergreenManager:
    """
    Beskytter vigtige dokumenter mod temporal decay.
    Manualer, blueprints og principper skal altid have fuld relevans.
    """
    def __init__(self):
        self.evergreen_patterns = [
            "BLUEPRINT.md",
            "IDENTITY.md",
            "SOUL.md",
            "CLAUDE.md",
            "KNB.manuals/",
            "rules/",
            "SPEC-"
        ]

    def is_evergreen(self, source_path):
        if not source_path:
            return False
        return any(pattern in source_path for pattern in self.evergreen_patterns)

    def protect_scores(self, points):
        """
        Gendanner original score for evergreen-filer hvis de er blevet decayet.
        """
        for p in points:
            source = p.get('payload', {}).get('source') or p.get('file_path')
            if self.is_evergreen(source):
                p['decay_factor'] = 1.0
                p['decayed_score'] = p.get('score', p.get('decayed_score', 0.0))
        return points

if __name__ == "__main__":
    manager = EvergreenManager()
    test_files = ["BLUEPRINT.md", "data/episodes.jsonl", "KNB.manuals/git.md", "scripts/memory.py"]
    for f in test_files:
        print(f"{f:<25} | Evergreen: {manager.is_evergreen(f)}")
