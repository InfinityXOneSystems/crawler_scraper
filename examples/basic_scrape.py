"""Basic scraping example."""

from crawler_scrapper import Scraper, ScraperConfig


def main():
    """Run a basic scrape example."""
    # Sample HTML for demonstration
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page</title>
        <meta name="description" content="This is an example page">
    </head>
    <body>
        <h1>Welcome to Example Page</h1>
        <h2>Section 1</h2>
        <p>This is some content in section 1.</p>
        <a href="/page1">Link 1</a>
        <h2>Section 2</h2>
        <p>This is some content in section 2.</p>
        <a href="/page2">Link 2</a>
        <img src="/image1.jpg" alt="Image 1">
    </body>
    </html>
    """
    
    # Configure the scraper
    config = ScraperConfig(
        parser="lxml",
        extract_text=True,
        extract_links=True,
        extract_images=True,
        extract_meta=True,
    )
    
    # Create scraper instance
    scraper = Scraper(config)
    
    # Scrape the HTML
    print("Scraping HTML...")
    result = scraper.scrape(sample_html, "https://example.com")
    
    # Display results
    print("\nScraping completed!")
    print(f"\nTitle: {result['text']['title']}")
    print(f"\nHeadings: {result['text']['headings']}")
    print(f"\nLinks found: {len(result['links'])}")
    for link in result['links']:
        print(f"  - {link['text']}: {link['href']}")
    
    print(f"\nImages found: {len(result['images'])}")
    for image in result['images']:
        print(f"  - {image['alt']}: {image['src']}")
    
    print(f"\nMeta tags: {result['meta']}")


if __name__ == "__main__":
    main()
