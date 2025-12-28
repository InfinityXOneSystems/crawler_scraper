from app.scraper import scrape_url
from app.config import get_config
from app.sync_orchestrator import orchestrate_sync
from app.change_detector import detect_changes
from app.ai_doc_agent import process_document
from app.governance import enforce_policies


def run_crawl(payload: dict):
    seed = payload.get("seed_url")
    industry = payload.get("industry", "generic")
    try:
        depth = int(payload.get("depth", 1))
    except Exception:
        depth = 1

    if not seed:
        return {"error": "seed_url required"}

    try:
        # Existing scraping logic
        config = get_config(industry)
        result = scrape_url(seed, config)

        # New integration: Document processing and governance
        processed_doc = process_document(result.get("content"))
        changes = detect_changes(processed_doc)
        enforce_policies(processed_doc, changes)

        orchestrate_sync(processed_doc)
    except Exception as e:
        return {"error": "crawl_failed", "reason": str(e)}

    return {
        "seed_url": seed,
        "industry": industry,
        "pages_crawled": 1,
        "content": result.get("content"),
        "metadata": {
            "content_length": result.get("content_length"),
        }
    }
