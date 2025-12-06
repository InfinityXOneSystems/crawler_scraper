"""Example of using the modular pipeline with integrations."""

from crawler_scrapper import Crawler, Scraper, ModuleManager
from crawler_scrapper.modules import DataValidatorModule, DataTransformerModule, RateLimiterModule
from crawler_scrapper.integrations import (
    AutoBuilderIntegration,
    FoundationIntegration,
    TaxonomyIntegration,
    GatewayIntegration,
)


def main():
    """Run a complete modular pipeline example."""
    print("Setting up modular crawler/scraper pipeline...\n")
    
    # Initialize module manager
    manager = ModuleManager()
    
    # Register modules
    print("Registering modules...")
    manager.register_module(
        "validator",
        DataValidatorModule({
            "required_fields": ["url", "content"],
            "min_content_length": 50,
        })
    )
    
    manager.register_module(
        "transformer",
        DataTransformerModule({
            "transformations": ["remove_nulls"],
        })
    )
    
    manager.register_module(
        "rate_limiter",
        RateLimiterModule({
            "requests_per_second": 2,
        })
    )
    
    # Register integrations
    print("Registering integrations...")
    manager.register_module(
        "auto_builder",
        AutoBuilderIntegration({
            "endpoint": "https://api.example.com/builder",
            "build_type": "web_content",
        })
    )
    
    manager.register_module(
        "foundation",
        FoundationIntegration({
            "storage_path": "/data/crawled",
            "schema_version": "1.0",
        })
    )
    
    manager.register_module(
        "taxonomy",
        TaxonomyIntegration({
            "default_categories": ["web_content"],
            "auto_classify": True,
        })
    )
    
    manager.register_module(
        "gateway",
        GatewayIntegration({
            "gateway_url": "https://api.example.com/gateway",
            "routing_rules": {
                "web_content": {
                    "destination": "content_processor",
                    "conditions": {"type": "html"},
                }
            },
        })
    )
    
    print(f"\nRegistered modules: {manager.list_modules()}")
    
    # Create sample data (simulating crawled page)
    sample_data = {
        "url": "https://example.com/page",
        "content": "This is some sample content from a crawled page.",
        "status_code": 200,
        "timestamp": 1234567890,
    }
    
    # Execute pipeline
    print("\nExecuting pipeline...")
    pipeline = [
        "rate_limiter",
        "validator",
        "transformer",
        "taxonomy",
        "foundation",
        "gateway",
        "auto_builder",
    ]
    
    result = manager.execute_pipeline(pipeline, sample_data)
    
    print("\nPipeline completed!")
    print(f"Final result: {result}")
    
    # Get module information
    print("\n\nModule Information:")
    for name, info in manager.get_all_module_info().items():
        print(f"\n{name}:")
        print(f"  Enabled: {info['enabled']}")
        print(f"  Config keys: {list(info['config'].keys())}")
    
    # Cleanup
    print("\n\nCleaning up...")
    manager.cleanup_all()
    print("Done!")


if __name__ == "__main__":
    main()
