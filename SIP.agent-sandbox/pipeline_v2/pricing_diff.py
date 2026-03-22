import hashlib
import json
from pathlib import Path

# Mock data
MOCK_PAGES = {
    "anthropic": "<html>Claude 4.5: $3/MTok Sonnet, $15/MTok Opus (New prices!)</html>",
    "openai": "<html>GPT-5.2: $2/MTok, $8/MTok</html>"
}

def check_pricing_poc(provider, current_html):
    """PoC for pricing diff checking."""
    snapshot_dir = Path("SIP.agent-sandbox/pipeline_v2/snapshots")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    hash_file = snapshot_dir / f"{provider}.hash"
    new_hash = hashlib.md5(current_html.encode()).hexdigest()
    
    print(f"Checking {provider} pricing...")
    
    if hash_file.exists():
        old_hash = hash_file.read_text().strip()
        if old_hash != new_hash:
            print(f"  [ALERT] Pricing page for {provider} has CHANGED!")
            print(f"  Old Hash: {old_hash}")
            print(f"  New Hash: {new_hash}")
            # Her ville man sende telegram/logge diff
            hash_file.write_text(new_hash)
            return True
        else:
            print(f"  [OK] No changes detected for {provider}.")
    else:
        print(f"  [INIT] First run for {provider}. Creating snapshot.")
        hash_file.write_text(new_hash)
        
    return False

if __name__ == "__main__":
    print("--- Pricing Diff-checker PoC ---")
    
    # Simuler første kørsel
    check_pricing_poc("anthropic", MOCK_PAGES["anthropic"])
    
    # Simuler ingen ændring
    print("\nSecond run (no change):")
    check_pricing_poc("anthropic", MOCK_PAGES["anthropic"])
    
    # Simuler en ændring
    print("\nThird run (PRICING CHANGE!):")
    changed_html = "<html>Claude 4.5: $2.5/MTok (SALE!)</html>"
    check_pricing_poc("anthropic", changed_html)
