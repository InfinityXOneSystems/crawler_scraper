"""Tests for the scraper module."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler_scrapper import Scraper, ScraperConfig


def test_scraper_initialization():
    """Test scraper initialization."""
    scraper = Scraper()
    assert scraper is not None
    assert scraper.config is not None


def test_scraper_with_config():
    """Test scraper with custom config."""
    config = ScraperConfig(
        parser="lxml",
        extract_text=True,
        extract_links=False,
    )
    scraper = Scraper(config)
    assert scraper.config.extract_text is True
    assert scraper.config.extract_links is False


def test_scraper_extract_text():
    """Test text extraction."""
    html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Title</h1>
            <h2>Subtitle</h2>
            <p>Some content</p>
        </body>
    </html>
    """
    
    scraper = Scraper()
    result = scraper.scrape(html)
    
    assert "text" in result
    assert result["text"]["title"] == "Test Page"
    assert "Main Title" in result["text"]["headings"]
    assert "Subtitle" in result["text"]["headings"]


def test_scraper_extract_links():
    """Test link extraction."""
    html = """
    <html>
        <body>
            <a href="/page1">Link 1</a>
            <a href="/page2" title="Page 2">Link 2</a>
        </body>
    </html>
    """
    
    scraper = Scraper()
    result = scraper.scrape(html)
    
    assert "links" in result
    assert len(result["links"]) == 2
    assert result["links"][0]["href"] == "/page1"
    assert result["links"][1]["title"] == "Page 2"


def test_scraper_extract_images():
    """Test image extraction."""
    html = """
    <html>
        <body>
            <img src="/image1.jpg" alt="Image 1">
            <img src="/image2.jpg" alt="Image 2" title="Second Image">
        </body>
    </html>
    """
    
    scraper = Scraper()
    result = scraper.scrape(html)
    
    assert "images" in result
    assert len(result["images"]) == 2
    assert result["images"][0]["src"] == "/image1.jpg"
    assert result["images"][1]["alt"] == "Image 2"


def test_scraper_custom_selectors():
    """Test custom CSS selectors."""
    html = """
    <html>
        <body>
            <div class="article">
                <h1 class="title">Article Title</h1>
                <div class="content">Article content</div>
            </div>
        </body>
    </html>
    """
    
    config = ScraperConfig(
        custom_selectors={
            "title": "h1.title",
            "content": "div.content",
        }
    )
    scraper = Scraper(config)
    result = scraper.scrape(html)
    
    assert "custom" in result
    assert "Article Title" in result["custom"]["title"]
    assert "Article content" in result["custom"]["content"]


def test_scraper_register_custom_extractor():
    """Test registering custom extractor."""
    def extract_custom(soup, html):
        return {"custom_data": "test"}
    
    scraper = Scraper()
    scraper.register_extractor("custom", extract_custom)
    
    result = scraper.scrape("<html><body>Test</body></html>")
    
    assert "extractors" in result
    assert "custom" in result["extractors"]
    assert result["extractors"]["custom"]["custom_data"] == "test"


if __name__ == "__main__":
    # Run tests
    test_scraper_initialization()
    test_scraper_with_config()
    test_scraper_extract_text()
    test_scraper_extract_links()
    test_scraper_extract_images()
    test_scraper_custom_selectors()
    test_scraper_register_custom_extractor()
    print("All tests passed!")
