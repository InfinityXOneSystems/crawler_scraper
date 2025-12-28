from __future__ import annotations

from typing import Dict, Any
from dataclasses import dataclass
from dataclasses import asdict
from vision_cortex.integration.headless_team import fetch_url, allowed_by_robots


@dataclass
class HeadlessCrawlerAgent:
    name: str = "headless_crawler"

    def run_task(self, context: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        url = payload.get("url")
        if not url:
            return {"success": False, "error": "Missing url in payload"}

        no_robots = payload.get("no_robots", False)
        dev_ok = context.get("dev_ok", False)
        if no_robots and not dev_ok:
            return {"success": False, "error": "no_robots requested but no dev_ok flag present"}

        if not no_robots:
            allowed = allowed_by_robots(url)
            if not allowed:
                return {"success": False, "error": "Blocked by robots.txt"}

        res = fetch_url(url, timeout=payload.get("timeout", 15))
        out = {
            "success": res.get("status") == "ok",
            "url": url,
            "http_status": res.get("http_status"),
            "content_length": res.get("content_length"),
            "duration": res.get("duration_seconds"),
        }
        if not out["success"]:
            out["error"] = res.get("error", "fetch_failed")
        else:
            out["excerpt"] = res.get("text_excerpt")

        return out
