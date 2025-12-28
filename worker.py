import logging

import asyncio
import json
import os
import time
from pathlib import Path
import requests
from playwright.async_api import async_playwright

OUT_DIR = Path("results/uncleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def fetch_and_save(url: str, use_credential_manager: bool = False, cm_url: str | None = None):
    token = None
    if use_credential_manager and cm_url:
        # try to fetch a test secret (expects authorization via env TOKEN)
        try:
            hdr = {}
            t = os.environ.get('CREDENTIAL_MANAGER_TOKEN')
            if t:
                hdr['Authorization'] = f'Bearer {t}'
            r = requests.get(f"{cm_url}/secret/test-secret", headers=hdr, timeout=10)
            if r.status_code == 200:
                token = r.json().get('secret')
        except Exception:
            token = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=15000)
            except Exception as e:
                await browser.close()
                raise RuntimeError(f"Navigation failed for {url}: {e}")
            html = await page.content()
            try:
                text = await page.inner_text('body')
            except Exception:
                text = ''
            await browser.close()
    except Exception as e:
        raise RuntimeError(f"Playwright fetch failed for {url}: {e}")

    ts = int(time.time())
    out = {
        'url': url,
        'fetched_at': ts,
        'html_length': len(html),
        'text_snippet': text[:500],
        'credential_token_present': bool(token),
    }
    fname = OUT_DIR / f"sample-{ts}.json"
    logging.info('Wrote', fname)
        json.dump(out, f, ensure_ascii=False, indent=2)
    logging.info('Wrote', fname)


def main():
    url = os.environ.get('WORKER_URL', 'https://example.com')
    cm = os.environ.get('CREDENTIAL_MANAGER_URL')
    use_cm = os.environ.get('USE_CREDENTIAL_MANAGER', 'false').lower() in ('1', 'true', 'yes')
    asyncio.run(fetch_and_save(url, use_credential_manager=use_cm, cm_url=cm))


if __name__ == '__main__':
    main()
