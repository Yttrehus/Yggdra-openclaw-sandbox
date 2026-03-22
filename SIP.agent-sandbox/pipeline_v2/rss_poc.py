import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# Definer Mock klasserne direkte i scriptet
class MockEntry:
    def __init__(self, title, link, days_ago, summary):
        self.title = title
        self.link = link
        self.published_parsed = time.gmtime(time.time() - 86400 * days_ago)
        self.summary = summary

class MockFeed:
    def __init__(self, name):
        if "Anthropic" in name:
            self.entries = [MockEntry('Claude 4.5 Released', 'https://anthropic.com/claude-4-5', 0, 'Anthropic announces the next generation of Claude.')]
        elif "OpenAI" in name:
            self.entries = [MockEntry('GPT-6 Preview', 'https://openai.com/gpt-6', 10, 'OpenAI gives a sneak peek at GPT-6.')]
        else:
            self.entries = []

class MockFeedParser:
    def parse(self, url):
        # Vi lader som om vi kender navnet baseret på URL for denne demo
        if "anthropic" in url: return MockFeed("Anthropic")
        if "openai" in url: return MockFeed("OpenAI")
        return type('obj', (object,), {'entries': []})

feedparser = MockFeedParser()

def fetch_rss_feeds(sources_data):
    """Hent nyeste posts fra RSS feeds (PoC)."""
    items = []
    feeds = sources_data.get("rss_feeds", [])
    now = datetime.now()

    print(f"--- Fetching RSS feeds at {now.strftime('%Y-%m-%d %H:%M:%S')} ---")

    for feed_cfg in feeds:
        print(f"Processing feed: {feed_cfg['name']}...")
        try:
            parsed = feedparser.parse(feed_cfg["url"])
            print(f"  [INFO] Parsed {len(parsed.entries)} entries.")
            for entry in parsed.entries[:5]:
                pub_date = time.strftime("%Y-%m-%d", entry.published_parsed)

                # Kun posts fra sidste 7 dage
                limit_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
                
                if pub_date >= limit_date:
                    items.append({
                        "source": f"rss/{feed_cfg['name']}",
                        "title": entry.title,
                        "url": entry.link,
                        "date": pub_date,
                        "summary": entry.summary[:300],
                    })
                    print(f"  [HIT] {entry.title} ({pub_date})")
                else:
                    print(f"  [SKIP] {entry.title} ({pub_date}) - too old")
        except Exception as e:
            print(f"  [ERROR] RSS {feed_cfg['name']} fejl: {e}")
    return items

if __name__ == "__main__":
    test_sources = {
        "rss_feeds": [
            {"name": "Anthropic Research", "url": "https://www.anthropic.com/research/rss", "priority": "high"},
            {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss/", "priority": "high"}
        ]
    }
    
    results = fetch_rss_feeds(test_sources)
    print(f"\nTotal items fetched: {len(results)}")
    print(json.dumps(results, indent=2))
