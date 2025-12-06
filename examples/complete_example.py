"""
Complete example demonstrating all features of the crawler_scrapper system.

This example shows:
1. Crawling web pages
2. Scraping structured data
3. Validating data quality
4. Transforming data
5. Classifying with taxonomy
6. Storing in foundation
7. Routing through gateway
8. Triggering builds
"""

from crawler_scrapper import Crawler, CrawlerConfig, Scraper, ScraperConfig, ModuleManager
from crawler_scrapper.modules import DataValidatorModule, DataTransformerModule, RateLimiterModule
from crawler_scrapper.integrations import (
    AutoBuilderIntegration,
    FoundationIntegration,
    TaxonomyIntegration,
    GatewayIntegration,
)


def main():
    """Run complete example with all features."""
    print("=" * 70)
    print("COMPLETE CRAWLER SCRAPPER SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # =========================================================================
    # STEP 1: Configure Crawler
    # =========================================================================
    print("\n[1/8] Configuring crawler...")
    crawler_config = CrawlerConfig(
        max_depth=1,  # Keep shallow for demo
        max_pages=5,
        delay=1.0,
        user_agent="CrawlerScrapperBot/0.1.0 (Demo)",
        follow_external_links=False,
    )
    crawler = Crawler(crawler_config)
    print("✓ Crawler configured")
    
    # =========================================================================
    # STEP 2: Configure Scraper
    # =========================================================================
    print("\n[2/8] Configuring scraper...")
    scraper_config = ScraperConfig(
        parser="lxml",
        extract_text=True,
        extract_links=True,
        extract_images=True,
        extract_meta=True,
        custom_selectors={
            "main_heading": "h1",
            "paragraphs": "p",
        }
    )
    scraper = Scraper(scraper_config)
    print("✓ Scraper configured")
    
    # =========================================================================
    # STEP 3: Setup Module Manager and Modules
    # =========================================================================
    print("\n[3/8] Setting up module pipeline...")
    manager = ModuleManager()
    
    # Add rate limiter
    manager.register_module(
        "rate_limiter",
        RateLimiterModule({
            "requests_per_second": 2,
            "burst_size": 5,
        })
    )
    
    # Add validator
    manager.register_module(
        "validator",
        DataValidatorModule({
            "required_fields": ["url", "status_code"],
            "min_content_length": 10,
            "allowed_status_codes": [200],
        })
    )
    
    # Add transformer
    manager.register_module(
        "transformer",
        DataTransformerModule({
            "transformations": ["remove_nulls"],
        })
    )
    
    print(f"✓ Registered {len(manager.list_modules())} modules")
    
    # =========================================================================
    # STEP 4: Setup Integrations
    # =========================================================================
    print("\n[4/8] Setting up integrations...")
    
    # Taxonomy for classification
    manager.register_module(
        "taxonomy",
        TaxonomyIntegration({
            "taxonomy_url": "https://api.example.com/taxonomy",
            "default_categories": ["web_content", "documentation"],
            "auto_classify": True,
        })
    )
    
    # Foundation for storage
    manager.register_module(
        "foundation",
        FoundationIntegration({
            "storage_path": "/data/crawled",
            "database_url": "postgresql://localhost/crawler_db",
            "schema_version": "1.0",
        })
    )
    
    # Gateway for routing
    manager.register_module(
        "gateway",
        GatewayIntegration({
            "gateway_url": "https://api.example.com/gateway",
            "routing_rules": {
                "documentation": {
                    "destination": "doc_processor",
                    "conditions": {"type": "documentation"}
                }
            },
            "retry_enabled": True,
            "max_retries": 3,
        })
    )
    
    # Auto builder for builds
    manager.register_module(
        "auto_builder",
        AutoBuilderIntegration({
            "endpoint": "https://api.example.com/builder",
            "api_key": "demo-api-key",
            "build_type": "documentation",
        })
    )
    
    print(f"✓ Registered {len(manager.list_modules())} total components")
    
    # =========================================================================
    # STEP 5: Simulate Crawling (using sample data for demo)
    # =========================================================================
    print("\n[5/8] Simulating crawl (using sample data)...")
    
    # In a real scenario, you would crawl actual websites:
    # results = crawler.crawl("https://example.com")
    
    # For demo, we'll create sample data
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Documentation Page</title>
        <meta name="description" content="API documentation">
        <meta name="keywords" content="api, documentation, reference">
    </head>
    <body>
        <h1>API Documentation</h1>
        <p>This is the main API documentation page.</p>
        <p>It contains information about all available endpoints.</p>
        <a href="/api/v1">Version 1 API</a>
        <a href="/api/v2">Version 2 API</a>
        <img src="/logo.png" alt="Company Logo">
    </body>
    </html>
    """
    
    simulated_crawl_result = {
        "url": "https://example.com/docs",
        "final_url": "https://example.com/docs",
        "status_code": 200,
        "content": sample_html,
        "headers": {"content-type": "text/html"},
        "depth": 0,
        "timestamp": 1234567890,
    }
    
    print("✓ Crawl completed (1 page)")
    
    # =========================================================================
    # STEP 6: Scrape Data
    # =========================================================================
    print("\n[6/8] Scraping structured data...")
    scraped_data = scraper.scrape(
        simulated_crawl_result["content"],
        url=simulated_crawl_result["url"]
    )
    
    # Merge crawl and scrape data
    combined_data = {**simulated_crawl_result, "scraped": scraped_data}
    
    print(f"✓ Extracted data from page")
    print(f"  - Title: {scraped_data['text']['title']}")
    print(f"  - Links: {len(scraped_data['links'])} found")
    print(f"  - Images: {len(scraped_data['images'])} found")
    print(f"  - Meta tags: {len(scraped_data['meta'])} found")
    
    # =========================================================================
    # STEP 7: Execute Pipeline
    # =========================================================================
    print("\n[7/8] Processing through module pipeline...")
    
    pipeline = [
        "rate_limiter",
        "validator",
        "transformer",
        "taxonomy",
        "foundation",
        "gateway",
        "auto_builder",
    ]
    
    print(f"Pipeline: {' → '.join(pipeline)}")
    
    try:
        result = manager.execute_pipeline(pipeline, combined_data)
        print("✓ Pipeline executed successfully")
        print(f"\nFinal Result:")
        print(f"  - Status: {result.get('status', 'N/A')}")
        print(f"  - Build ID: {result.get('build_id', 'N/A')}")
        print(f"  - Message: {result.get('message', 'N/A')}")
    except Exception as e:
        print(f"✗ Pipeline error: {e}")
        result = None
    
    # =========================================================================
    # STEP 8: Display Statistics and Info
    # =========================================================================
    print("\n[8/8] System statistics...")
    
    # Module information
    print("\nRegistered Modules:")
    for name, info in manager.get_all_module_info().items():
        print(f"  • {name:20s} - Enabled: {info['enabled']}")
    
    # Crawler stats (if we had crawled)
    # stats = crawler.get_stats()
    # print(f"\nCrawler Statistics:")
    # print(f"  - Pages visited: {stats['total_pages_visited']}")
    # print(f"  - Results collected: {stats['results_collected']}")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nThis example demonstrated:")
    print("✓ Crawler configuration and usage")
    print("✓ Scraper with custom selectors")
    print("✓ Module pipeline with validation and transformation")
    print("✓ Integration with external systems (taxonomy, foundation, gateway, builder)")
    print("✓ End-to-end data processing workflow")
    print("\nFor real usage, replace sample data with actual web crawling.")
    print("See other examples in the examples/ directory for specific use cases.")
    
    # Cleanup
    manager.cleanup_all()
    print("\n✓ Cleanup completed")


if __name__ == "__main__":
    main()
