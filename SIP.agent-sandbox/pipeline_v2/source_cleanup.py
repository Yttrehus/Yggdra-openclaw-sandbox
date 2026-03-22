import re
import json

# Fra PIPELINE_DESIGN.md
NOISE_PATTERNS = [
    r"^ukendt",
    r"^ikke specificeret",
    r"^tools/platforms$",
    r"^prize$",
]

def clean_discovered(sources):
    """Fjern low-quality discovered sources (PoC)."""
    cleaned = []
    removed_count = 0
    
    print("--- Source Cleanup PoC ---")
    
    for src in sources.get("discovered_sources", []):
        name = src.get("name", "").lower()
        if not any(re.match(p, name) for p in NOISE_PATTERNS):
            cleaned.append(src)
        else:
            print(f"  [REMOVED] {src.get('name')}")
            removed_count += 1
            
    print(f"\nCleanup finished. Removed {removed_count} noise entries.")
    sources["discovered_sources"] = cleaned
    return sources

if __name__ == "__main__":
    # Test data baseret på "Problem" beskrivelsen i PIPELINE_DESIGN.md
    test_sources = {
        "discovered_sources": [
            {"name": "prize", "url": "http://example.com/1"},
            {"name": "Tools/Platforms", "url": "http://example.com/2"},
            {"name": "Ukendt kanal", "url": "http://example.com/3"},
            {"name": "Valid Source", "url": "http://example.com/4"},
            {"name": "Anthropic Blog", "url": "http://example.com/5"},
        ]
    }
    
    cleaned = clean_discovered(test_sources)
    print("\nResulting sources:")
    for s in cleaned["discovered_sources"]:
        print(f"  - {s['name']}")
