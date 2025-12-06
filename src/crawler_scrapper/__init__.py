"""
Modular Crawler and Scraper System

A flexible, extensible system for web crawling and scraping that integrates
with auto builder, foundation, taxonomy, gateway and other modular systems.
"""

__version__ = "0.1.0"

from .core.crawler import Crawler, CrawlerConfig
from .core.scraper import Scraper, ScraperConfig
from .core.module_manager import ModuleManager

__all__ = [
    "Crawler",
    "CrawlerConfig",
    "Scraper",
    "ScraperConfig",
    "ModuleManager",
]
