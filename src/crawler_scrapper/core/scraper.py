"""Core scraper implementation."""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from bs4 import BeautifulSoup


@dataclass
class ScraperConfig:
    """Configuration for the scraper."""
    
    parser: str = "lxml"
    extract_text: bool = True
    extract_links: bool = True
    extract_images: bool = True
    extract_meta: bool = True
    custom_selectors: Dict[str, str] = field(default_factory=dict)


class Scraper:
    """
    Modular web scraper with configurable extraction rules.
    
    This scraper can be extended with custom parsers and integrated
    with taxonomy systems and other downstream processors.
    """
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Initialize the scraper.
        
        Args:
            config: Scraper configuration
        """
        self.config = config or ScraperConfig()
        self.custom_extractors: Dict[str, Callable] = {}
    
    def scrape(self, html: str, url: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape data from HTML content.
        
        Args:
            html: HTML content to scrape
            url: Optional URL of the page
            
        Returns:
            Dictionary containing scraped data
        """
        soup = BeautifulSoup(html, self.config.parser)
        result: Dict[str, Any] = {"url": url}
        
        if self.config.extract_text:
            result["text"] = self._extract_text(soup)
        
        if self.config.extract_links:
            result["links"] = self._extract_links(soup)
        
        if self.config.extract_images:
            result["images"] = self._extract_images(soup)
        
        if self.config.extract_meta:
            result["meta"] = self._extract_meta(soup)
        
        # Apply custom selectors
        if self.config.custom_selectors:
            result["custom"] = self._apply_custom_selectors(soup)
        
        # Apply custom extractors
        if self.custom_extractors:
            result["extractors"] = self._apply_custom_extractors(soup, html)
        
        return result
    
    def _extract_text(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract text content from the page."""
        return {
            "title": soup.title.string if soup.title else "",
            "body": soup.get_text(strip=True, separator=" "),
            "headings": [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])],
        }
    
    def _extract_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all links from the page."""
        links = []
        for tag in soup.find_all("a", href=True):
            links.append({
                "href": tag["href"],
                "text": tag.get_text(strip=True),
                "title": tag.get("title", ""),
            })
        return links
    
    def _extract_images(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all images from the page."""
        images = []
        for tag in soup.find_all("img", src=True):
            images.append({
                "src": tag["src"],
                "alt": tag.get("alt", ""),
                "title": tag.get("title", ""),
            })
        return images
    
    def _extract_meta(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from the page."""
        meta = {}
        
        # Extract meta tags
        for tag in soup.find_all("meta"):
            name = tag.get("name") or tag.get("property")
            content = tag.get("content")
            if name and content:
                meta[name] = content
        
        return meta
    
    def _apply_custom_selectors(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Apply custom CSS selectors."""
        results = {}
        for name, selector in self.config.custom_selectors.items():
            elements = soup.select(selector)
            results[name] = [elem.get_text(strip=True) for elem in elements]
        return results
    
    def _apply_custom_extractors(self, soup: BeautifulSoup, html: str) -> Dict[str, Any]:
        """Apply custom extractor functions."""
        results = {}
        for name, extractor in self.custom_extractors.items():
            try:
                results[name] = extractor(soup, html)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results
    
    def register_extractor(self, name: str, extractor: Callable) -> None:
        """
        Register a custom extractor function.
        
        Args:
            name: Name of the extractor
            extractor: Function that takes (soup, html) and returns extracted data
        """
        self.custom_extractors[name] = extractor
    
    def unregister_extractor(self, name: str) -> None:
        """
        Remove a custom extractor.
        
        Args:
            name: Name of the extractor to remove
        """
        if name in self.custom_extractors:
            del self.custom_extractors[name]
