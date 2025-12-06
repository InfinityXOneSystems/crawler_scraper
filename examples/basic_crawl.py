"""Basic crawling example."""

from crawler_scrapper import Crawler, CrawlerConfig


def main():
    """Run a basic crawl example."""
    # Configure the crawler
    config = CrawlerConfig(
        max_depth=2,
        max_pages=10,
        delay=1.0,
        follow_external_links=False,
    )
    
    # Create crawler instance
    crawler = Crawler(config)
    
    # Start crawling (example URL - replace with actual URL)
    print("Starting crawl...")
    results = crawler.crawl("https://example.com")
    
    # Display results
    print(f"\nCrawl completed!")
    print(f"Pages visited: {len(results)}")
    
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result['url']}")
        print(f"   Status: {result['status_code']}")
        print(f"   Depth: {result['depth']}")
        print(f"   Content length: {len(result['content'])} chars")
    
    # Get statistics
    stats = crawler.get_stats()
    print(f"\nStatistics:")
    print(f"  Total pages visited: {stats['total_pages_visited']}")
    print(f"  Results collected: {stats['results_collected']}")


if __name__ == "__main__":
    main()
