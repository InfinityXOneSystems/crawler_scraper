import os
import json
import requests
from bs4 import BeautifulSoup
from app.normalizer import normalize_text
from app.config import OUTPUT_DIR

DEFAULT_TIMEOUT = 10
MAX_CHARS = 20000
RESULTS_DIR = OUTPUT_DIR
os.makedirs(RESULTS_DIR, exist_ok=True)

def scrape_url(url: str, config: dict) -> dict:
    headers = {
        "User-Agent": config.get("user_agent", "InfinityCrawler/1.0")
    }
    try:
        r = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Request failed for {url}: {e}")

    try:
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        normalized_text = normalize_text(text[:MAX_CHARS])
    except Exception as e:
        raise RuntimeError(f"Failed to parse HTML from {url}: {e}")

    # Save snapshot
    snapshot = {
        'url': url,
        'content': normalized_text,
        'content_length': len(normalized_text),
    }
    fname = os.path.join(RESULTS_DIR, f"scrape_{abs(hash(url))}.json")
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    return snapshot
