# Crawler Scrapper

A modular, extensible crawler and scraper system designed to integrate seamlessly with auto builder, foundation, taxonomy, gateway, and various other modular systems.

## Overview

This repository houses a flexible web crawling and scraping framework that can be extended with custom modules and integrated with external systems. The architecture is designed to be modular, allowing you to:

- Crawl websites with configurable depth and rate limiting
- Scrape and extract structured data from web pages
- Process data through custom modules and pipelines
- Integrate with external systems through standardized interfaces
- Build complex data processing workflows

## Features

### Core Components

- **Crawler**: Configurable web crawler with depth control, rate limiting, and domain filtering
- **Scraper**: Flexible data extraction with support for custom selectors and extractors
- **Module Manager**: Dynamic module loading and pipeline execution
- **Base Module**: Standard interface for creating custom modules

### Built-in Modules

- **Data Validator**: Validate crawled data against quality standards
- **Data Transformer**: Transform data formats and structures
- **Rate Limiter**: Control request rates to respect server resources

### Integration Interfaces

- **Auto Builder Integration**: Send crawled data to auto builder system
- **Foundation Integration**: Store and manage data in foundation system
- **Taxonomy Integration**: Classify and tag data using taxonomy system
- **Gateway Integration**: Route data through gateway to other services

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Install from source

```bash
git clone https://github.com/InfinityXOneSystems/crawler_scrapper.git
cd crawler_scrapper
pip install -r requirements.txt
pip install -e .
```

### Install dependencies only

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Crawling

```python
from crawler_scrapper import Crawler, CrawlerConfig

# Configure the crawler
config = CrawlerConfig(
    max_depth=2,
    max_pages=10,
    delay=1.0,
)

# Create and run crawler
crawler = Crawler(config)
results = crawler.crawl("https://example.com")

print(f"Crawled {len(results)} pages")
```

### Basic Scraping

```python
from crawler_scrapper import Scraper, ScraperConfig

# Configure the scraper
config = ScraperConfig(
    extract_text=True,
    extract_links=True,
    extract_images=True,
)

# Create and use scraper
scraper = Scraper(config)
data = scraper.scrape(html_content, url="https://example.com")

print(f"Extracted {len(data['links'])} links")
```

### Modular Pipeline

```python
from crawler_scrapper import ModuleManager
from crawler_scrapper.modules import DataValidatorModule
from crawler_scrapper.integrations import TaxonomyIntegration

# Initialize module manager
manager = ModuleManager()

# Register modules
manager.register_module("validator", DataValidatorModule())
manager.register_module("taxonomy", TaxonomyIntegration())

# Execute pipeline
result = manager.execute_pipeline(
    ["validator", "taxonomy"],
    data
)
```

## Configuration

Configuration can be provided via YAML files or directly in code. See `config/example_config.yaml` for a complete example.

### Crawler Configuration

```yaml
crawler:
  max_depth: 3
  max_pages: 100
  delay: 1.0
  user_agent: "CrawlerScrapperBot/0.1.0"
  timeout: 30
  follow_external_links: false
  allowed_domains:
    - example.com
```

### Scraper Configuration

```yaml
scraper:
  parser: lxml
  extract_text: true
  extract_links: true
  extract_images: true
  extract_meta: true
  custom_selectors:
    article_title: "h1.title"
    article_content: "div.content"
```

### Module Configuration

```yaml
modules:
  data_validator:
    enabled: true
    required_fields:
      - url
      - content
    min_content_length: 100
```

## Architecture

### Modular Design

The system is built on a modular architecture:

```
crawler_scrapper/
├── core/                 # Core components
│   ├── crawler.py       # Web crawler
│   ├── scraper.py       # Data scraper
│   ├── base_module.py   # Module interface
│   └── module_manager.py # Module management
├── modules/             # Built-in modules
│   ├── data_validator.py
│   ├── data_transformer.py
│   └── rate_limiter.py
├── integrations/        # External system integrations
│   ├── auto_builder.py
│   ├── foundation.py
│   ├── taxonomy.py
│   └── gateway.py
└── utils/              # Utility functions
    ├── config_loader.py
    └── url_utils.py
```

### Integration Points

The system provides standardized interfaces for integration with:

1. **Auto Builder**: Automated build and deployment system
2. **Foundation**: Data storage and management layer
3. **Taxonomy**: Classification and tagging system
4. **Gateway**: Data routing and distribution

Each integration implements the `BaseModule` interface, ensuring consistency across all integrations.

## Examples

See the `examples/` directory for complete working examples:

- `basic_crawl.py`: Simple web crawling
- `basic_scrape.py`: Simple data scraping
- `modular_pipeline.py`: Complete modular pipeline with integrations

Run examples:

```bash
python examples/basic_crawl.py
python examples/basic_scrape.py
python examples/modular_pipeline.py
```

## Creating Custom Modules

Extend the system with custom modules:

```python
from crawler_scrapper.core import BaseModule

class MyCustomModule(BaseModule):
    def initialize(self) -> bool:
        # Initialize your module
        return True
    
    def execute(self, data):
        # Process data
        return processed_data
    
    def cleanup(self):
        # Cleanup resources
        pass

# Register and use
manager.register_module("custom", MyCustomModule(config))
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Style

This project follows PEP 8 style guidelines.

## Integration with Other Systems

### Auto Builder

The auto builder integration allows crawled data to trigger automated builds:

```python
from crawler_scrapper.integrations import AutoBuilderIntegration

integration = AutoBuilderIntegration({
    "endpoint": "https://builder.example.com/api",
    "api_key": "your-key",
    "build_type": "web_content"
})

result = integration.execute(crawled_data)
```

### Foundation

Store and manage crawled data in the foundation system:

```python
from crawler_scrapper.integrations import FoundationIntegration

integration = FoundationIntegration({
    "storage_path": "/data/crawled",
    "database_url": "postgresql://localhost/db"
})

result = integration.execute(crawled_data)
```

### Taxonomy

Automatically classify and tag content:

```python
from crawler_scrapper.integrations import TaxonomyIntegration

integration = TaxonomyIntegration({
    "default_categories": ["web_content"],
    "auto_classify": True
})

classified_data = integration.execute(crawled_data)
```

### Gateway

Route data to appropriate downstream services:

```python
from crawler_scrapper.integrations import GatewayIntegration

integration = GatewayIntegration({
    "gateway_url": "https://gateway.example.com",
    "routing_rules": {
        "articles": {
            "destination": "article_processor",
            "conditions": {"type": "article"}
        }
    }
})

result = integration.execute(crawled_data)
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is part of the InfinityXOneSystems modular architecture.

## Links

- **Repository**: https://github.com/InfinityXOneSystems/crawler_scrapper
- **Related Projects**:
  - Auto Builder
  - Foundation
  - Taxonomy
  - Gateway