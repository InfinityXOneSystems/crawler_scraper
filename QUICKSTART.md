# Quick Start Guide

This guide will help you get started with the Crawler Scrapper system quickly.

## Installation

### Option 1: Install from source

```bash
git clone https://github.com/InfinityXOneSystems/crawler_scrapper.git
cd crawler_scrapper
pip install -r requirements.txt
pip install -e .
```

### Option 2: Install dependencies only

```bash
pip install -r requirements.txt
```

## 5-Minute Tutorial

### 1. Basic Web Scraping

Extract data from HTML content:

```python
from crawler_scrapper import Scraper

# Create scraper
scraper = Scraper()

# Your HTML content
html = """
<html>
    <head><title>My Page</title></head>
    <body>
        <h1>Welcome</h1>
        <a href="/page1">Link 1</a>
    </body>
</html>
"""

# Scrape it
result = scraper.scrape(html)

# Access extracted data
print(result['text']['title'])  # "My Page"
print(result['links'])          # List of links
```

### 2. Web Crawling

Crawl multiple pages from a website:

```python
from crawler_scrapper import Crawler, CrawlerConfig

# Configure crawler
config = CrawlerConfig(
    max_depth=2,
    max_pages=10,
    delay=1.0
)

# Create and run crawler
crawler = Crawler(config)
results = crawler.crawl("https://example.com")

# Process results
for page in results:
    print(f"URL: {page['url']}")
    print(f"Status: {page['status_code']}")
```

### 3. Using Modules

Add validation and transformation:

```python
from crawler_scrapper import ModuleManager
from crawler_scrapper.modules import DataValidatorModule, DataTransformerModule

# Create module manager
manager = ModuleManager()

# Register modules
manager.register_module("validator", DataValidatorModule({
    "required_fields": ["url", "content"]
}))

manager.register_module("transformer", DataTransformerModule({
    "transformations": ["remove_nulls"]
}))

# Process data through pipeline
data = {"url": "https://example.com", "content": "...", "null_field": None}
result = manager.execute_pipeline(["validator", "transformer"], data)
```

### 4. Integration with External Systems

Connect to other systems:

```python
from crawler_scrapper import ModuleManager
from crawler_scrapper.integrations import TaxonomyIntegration, FoundationIntegration

manager = ModuleManager()

# Add taxonomy classification
manager.register_module("taxonomy", TaxonomyIntegration({
    "default_categories": ["web_content"]
}))

# Add data storage
manager.register_module("foundation", FoundationIntegration({
    "storage_path": "/data/crawled"
}))

# Process through integrations
result = manager.execute_pipeline(["taxonomy", "foundation"], data)
```

## Common Use Cases

### Use Case 1: Crawl and Store Data

```python
from crawler_scrapper import Crawler, Scraper, ModuleManager
from crawler_scrapper.integrations import FoundationIntegration

# Setup
crawler = Crawler()
scraper = Scraper()
manager = ModuleManager()
manager.register_module("storage", FoundationIntegration())

# Crawl
pages = crawler.crawl("https://example.com")

# Process each page
for page in pages:
    # Scrape structured data
    data = scraper.scrape(page['content'], page['url'])
    
    # Store it
    manager.execute_module("storage", data)
```

### Use Case 2: Extract and Classify Content

```python
from crawler_scrapper import Scraper, ScraperConfig, ModuleManager
from crawler_scrapper.integrations import TaxonomyIntegration

# Setup scraper with custom selectors
scraper = Scraper(ScraperConfig(
    custom_selectors={
        "article_title": "h1.title",
        "article_body": "div.content"
    }
))

# Setup taxonomy
manager = ModuleManager()
manager.register_module("classify", TaxonomyIntegration())

# Process
data = scraper.scrape(html_content)
classified = manager.execute_module("classify", data)
```

### Use Case 3: Build Complete Pipeline

```python
from crawler_scrapper import Crawler, Scraper, ModuleManager
from crawler_scrapper.modules import DataValidatorModule
from crawler_scrapper.integrations import *

# Setup crawler and scraper
crawler = Crawler()
scraper = Scraper()

# Setup pipeline
manager = ModuleManager()
manager.register_module("validator", DataValidatorModule())
manager.register_module("taxonomy", TaxonomyIntegration())
manager.register_module("foundation", FoundationIntegration())
manager.register_module("gateway", GatewayIntegration())
manager.register_module("builder", AutoBuilderIntegration())

# Execute
pages = crawler.crawl("https://example.com")
for page in pages:
    data = scraper.scrape(page['content'], page['url'])
    result = manager.execute_pipeline([
        "validator",
        "taxonomy",
        "foundation",
        "gateway",
        "builder"
    ], data)
```

## Configuration

### Using YAML Configuration

Create a `config.yaml`:

```yaml
crawler:
  max_depth: 3
  max_pages: 100
  delay: 1.0

scraper:
  extract_text: true
  extract_links: true
  custom_selectors:
    title: "h1.title"
```

Load and use it:

```python
from crawler_scrapper.utils import load_config
from crawler_scrapper import Crawler, CrawlerConfig

config_data = load_config("config.yaml")
crawler_config = CrawlerConfig(**config_data['crawler'])
crawler = Crawler(crawler_config)
```

## Next Steps

1. **Read the Documentation**: Check out [README.md](README.md) for detailed information
2. **Explore Examples**: Look at examples in the `examples/` directory
3. **API Reference**: See [API.md](API.md) for complete API documentation
4. **Architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
5. **Contribute**: Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute to the project

## Getting Help

- Check the [API documentation](API.md)
- Look at [example code](examples/)
- Open an issue on GitHub
- Read the architecture documentation

## Tips

1. **Start Small**: Begin with basic crawling/scraping, then add modules
2. **Test Incrementally**: Test each component before building complex pipelines
3. **Use Configuration Files**: Keep your configs in YAML files for easier management
4. **Respect Robots.txt**: Always respect website policies
5. **Rate Limiting**: Use appropriate delays to avoid overwhelming servers

## Common Issues

### Import Errors

If you get import errors, make sure you've installed the package:
```bash
pip install -e .
```

### Missing Dependencies

Install all dependencies:
```bash
pip install -r requirements.txt
```

### Slow Crawling

Adjust the delay in `CrawlerConfig`:
```python
config = CrawlerConfig(delay=0.5)  # Faster, but be respectful
```

Happy crawling and scraping!
