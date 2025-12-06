"""Core components for the crawler and scraper system."""

from .crawler import Crawler, CrawlerConfig
from .scraper import Scraper, ScraperConfig
from .module_manager import ModuleManager
from .base_module import BaseModule

__all__ = [
    "Crawler",
    "CrawlerConfig",
    "Scraper",
    "ScraperConfig",
    "ModuleManager",
    "BaseModule",
]
