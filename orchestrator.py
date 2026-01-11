import logging

import asyncio
from typing import List

from vision_cortex.integration.headless_team import fetch_url
from crawler.engine import crawl_urls


def needs_render(fetch_result: dict) -> bool:
    # Simple heuristics: scripts present in excerpt or large HTML content implied
    excerpt = (fetch_result.get("text_excerpt") or "").lower()
    cl = fetch_result.get("content_length") or 0
    if cl > 10000 and len(excerpt) < 500:
        return True
    if "<script" in excerpt:
        return True
    return False


async def _render_urls(urls: List[str], concurrency: int = 2):
    await crawl_urls(urls, concurrency=concurrency)


def orchestrate_from_seed(seed_file: str, concurrency: int = 2):
    import yaml
    with open(seed_file, "r", encoding="utf-8") as f:
        seed = yaml.safe_load(f)
    urls = [s.get("url") for s in seed.get("sources", []) if s.get("url")]

    to_render = []
    for u in urls:
        res = fetch_url(u)
        logging.info(f"fetch {u}: status={res.get('status')} http={res.get('http_status')} len={res.get('content_length')}")
        if res.get("status") == "ok" and needs_render(res):
            to_render.append(u)

    if to_render:
        logging.info(f"Dispatching {len(to_render)} URLs to Playwright engine")
        asyncio.run(_render_urls(to_render, concurrency=concurrency))
    else:
        logging.info("No URLs required rendering")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--seed", default="crawler/seeds/business_loans.yaml")
    p.add_argument("--concurrency", type=int, default=2)
    args = p.parse_args()
    orchestrate_from_seed(args.seed, concurrency=args.concurrency)
