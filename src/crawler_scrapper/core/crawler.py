"""Core crawler implementation."""

import time
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
import requests
from urllib.parse import urljoin, urlparse


@dataclass
class CrawlerConfig:
    """Configuration for the crawler."""
    
    max_depth: int = 3
    max_pages: int = 100
    delay: float = 1.0
    user_agent: str = "CrawlerScrapperBot/0.1.0"
    timeout: int = 30
    follow_external_links: bool = False
    allowed_domains: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set default headers if not provided."""
        if not self.headers:
            self.headers = {"User-Agent": self.user_agent}
        elif "User-Agent" not in self.headers:
            self.headers["User-Agent"] = self.user_agent


class Crawler:
    """
    Modular web crawler with configurable behavior.
    
    This crawler can be extended and integrated with other systems like
    auto builder, foundation, taxonomy, and gateway.
    """
    
    def __init__(self, config: Optional[CrawlerConfig] = None):
        """
        Initialize the crawler.
        
        Args:
            config: Crawler configuration
        """
        self.config = config or CrawlerConfig()
        self.visited_urls: Set[str] = set()
        self.to_visit: List[tuple] = []
        self.results: List[Dict[str, Any]] = []
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)
    
    def crawl(self, start_url: str) -> List[Dict[str, Any]]:
        """
        Start crawling from the given URL.
        
        Args:
            start_url: The URL to start crawling from
            
        Returns:
            List of crawled page data
        """
        self.to_visit = [(start_url, 0)]
        self.visited_urls = set()
        self.results = []
        
        while self.to_visit and len(self.visited_urls) < self.config.max_pages:
            url, depth = self.to_visit.pop(0)
            
            if url in self.visited_urls or depth > self.config.max_depth:
                continue
            
            page_data = self._fetch_page(url, depth)
            if page_data:
                self.results.append(page_data)
                self.visited_urls.add(url)
                
                # Extract and queue links
                if depth < self.config.max_depth:
                    links = self._extract_links(page_data["content"], url)
                    for link in links:
                        if link not in self.visited_urls:
                            self.to_visit.append((link, depth + 1))
            
            # Respect rate limiting
            time.sleep(self.config.delay)
        
        return self.results
    
    def _fetch_page(self, url: str, depth: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single page.
        
        Args:
            url: URL to fetch
            depth: Current crawl depth
            
        Returns:
            Dictionary containing page data or None if failed
        """
        try:
            response = self.session.get(
                url,
                timeout=self.config.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            return {
                "url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "content": response.text,
                "headers": dict(response.headers),
                "depth": depth,
                "timestamp": time.time(),
            }
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract links from HTML content.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, "lxml")
        links = []
        base_domain = urlparse(base_url).netloc
        
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)
            
            # Skip non-http(s) links
            if parsed.scheme not in ["http", "https"]:
                continue
            
            # Check domain restrictions
            if not self.config.follow_external_links:
                if parsed.netloc != base_domain:
                    continue
            
            if self.config.allowed_domains:
                if not any(domain in parsed.netloc for domain in self.config.allowed_domains):
                    continue
            
            links.append(absolute_url)
        
        return links
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get crawling statistics.
        
        Returns:
            Dictionary containing crawl statistics
        """
        return {
            "total_pages_visited": len(self.visited_urls),
            "pages_in_queue": len(self.to_visit),
            "results_collected": len(self.results),
        }
