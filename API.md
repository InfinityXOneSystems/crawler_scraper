# API Documentation

## Core API

### Crawler

The `Crawler` class provides web crawling functionality.

#### CrawlerConfig

Configuration dataclass for the crawler.

**Parameters:**
- `max_depth` (int): Maximum crawl depth (default: 3)
- `max_pages` (int): Maximum number of pages to crawl (default: 100)
- `delay` (float): Delay between requests in seconds (default: 1.0)
- `user_agent` (str): User agent string (default: "CrawlerScrapperBot/0.1.0")
- `timeout` (int): Request timeout in seconds (default: 30)
- `follow_external_links` (bool): Follow links to external domains (default: False)
- `allowed_domains` (List[str]): List of allowed domains (default: [])
- `headers` (Dict[str, str]): Custom HTTP headers (default: {})

**Example:**
```python
config = CrawlerConfig(
    max_depth=2,
    max_pages=50,
    delay=1.5,
    follow_external_links=False,
    allowed_domains=["example.com"]
)
```

#### Crawler

Main crawler class.

**Constructor:**
```python
Crawler(config: Optional[CrawlerConfig] = None)
```

**Methods:**

##### crawl(start_url: str) -> List[Dict[str, Any]]

Start crawling from the given URL.

**Parameters:**
- `start_url` (str): The URL to start crawling from

**Returns:**
- List[Dict[str, Any]]: List of crawled page data

**Example:**
```python
crawler = Crawler(config)
results = crawler.crawl("https://example.com")
```

##### get_stats() -> Dict[str, Any]

Get crawling statistics.

**Returns:**
- Dict containing:
  - `total_pages_visited` (int): Number of pages visited
  - `pages_in_queue` (int): Number of pages still queued
  - `results_collected` (int): Number of results collected

### Scraper

The `Scraper` class provides data extraction functionality.

#### ScraperConfig

Configuration dataclass for the scraper.

**Parameters:**
- `parser` (str): HTML parser to use (default: "lxml")
- `extract_text` (bool): Extract text content (default: True)
- `extract_links` (bool): Extract links (default: True)
- `extract_images` (bool): Extract images (default: True)
- `extract_meta` (bool): Extract meta tags (default: True)
- `custom_selectors` (Dict[str, str]): Custom CSS selectors (default: {})

**Example:**
```python
config = ScraperConfig(
    parser="lxml",
    extract_text=True,
    custom_selectors={
        "title": "h1.title",
        "content": "div.content"
    }
)
```

#### Scraper

Main scraper class.

**Constructor:**
```python
Scraper(config: Optional[ScraperConfig] = None)
```

**Methods:**

##### scrape(html: str, url: Optional[str] = None) -> Dict[str, Any]

Scrape data from HTML content.

**Parameters:**
- `html` (str): HTML content to scrape
- `url` (Optional[str]): URL of the page

**Returns:**
- Dict containing extracted data:
  - `url` (str): Page URL
  - `text` (Dict): Extracted text content
  - `links` (List[Dict]): Extracted links
  - `images` (List[Dict]): Extracted images
  - `meta` (Dict): Meta tags
  - `custom` (Dict): Custom selector results
  - `extractors` (Dict): Custom extractor results

**Example:**
```python
scraper = Scraper(config)
result = scraper.scrape(html_content, url="https://example.com")
```

##### register_extractor(name: str, extractor: Callable) -> None

Register a custom extractor function.

**Parameters:**
- `name` (str): Name of the extractor
- `extractor` (Callable): Function that takes (soup, html) and returns extracted data

**Example:**
```python
def extract_price(soup, html):
    return soup.select_one(".price").text

scraper.register_extractor("price", extract_price)
```

##### unregister_extractor(name: str) -> None

Remove a custom extractor.

**Parameters:**
- `name` (str): Name of the extractor to remove

### ModuleManager

The `ModuleManager` class manages modules and pipelines.

**Constructor:**
```python
ModuleManager()
```

**Methods:**

##### register_module(name: str, module: BaseModule, config: Optional[Dict] = None) -> None

Register a module with the manager.

**Parameters:**
- `name` (str): Name to register the module under
- `module` (BaseModule): Module instance to register
- `config` (Optional[Dict]): Optional configuration

**Example:**
```python
manager = ModuleManager()
manager.register_module("validator", DataValidatorModule(config))
```

##### unregister_module(name: str) -> None

Unregister and cleanup a module.

**Parameters:**
- `name` (str): Name of the module to unregister

##### get_module(name: str) -> Optional[BaseModule]

Get a registered module by name.

**Parameters:**
- `name` (str): Name of the module

**Returns:**
- Optional[BaseModule]: Module instance or None

##### list_modules() -> List[str]

List all registered module names.

**Returns:**
- List[str]: List of module names

##### execute_module(name: str, data: Any) -> Any

Execute a specific module.

**Parameters:**
- `name` (str): Name of the module to execute
- `data` (Any): Input data

**Returns:**
- Any: Output from the module

**Raises:**
- ValueError: If module not found or not enabled

##### execute_pipeline(module_names: List[str], data: Any) -> Any

Execute a pipeline of modules in sequence.

**Parameters:**
- `module_names` (List[str]): List of module names in execution order
- `data` (Any): Initial input data

**Returns:**
- Any: Final output after all modules

**Example:**
```python
result = manager.execute_pipeline(
    ["validator", "transformer", "taxonomy"],
    data
)
```

##### get_all_module_info() -> Dict[str, Dict[str, Any]]

Get information about all registered modules.

**Returns:**
- Dict mapping module names to their info

##### cleanup_all() -> None

Cleanup all registered modules.

## BaseModule Interface

All modules must inherit from `BaseModule` and implement these methods:

### initialize() -> bool

Initialize the module.

**Returns:**
- bool: True if initialization successful

### execute(data: Any) -> Any

Execute the module's main functionality.

**Parameters:**
- `data` (Any): Input data

**Returns:**
- Any: Processed output data

### cleanup() -> None

Clean up any resources used by the module.

### get_info() -> Dict[str, Any]

Get information about the module.

**Returns:**
- Dict containing module metadata

## Built-in Modules

### DataValidatorModule

Validates crawled/scraped data.

**Configuration:**
- `required_fields` (List[str]): Required fields in data
- `min_content_length` (int): Minimum content length
- `allowed_status_codes` (List[int]): Allowed HTTP status codes

**Example:**
```python
validator = DataValidatorModule({
    "required_fields": ["url", "content"],
    "min_content_length": 100,
    "allowed_status_codes": [200, 201]
})
```

### DataTransformerModule

Transforms data formats and structures.

**Configuration:**
- `transformations` (List[str]): List of transformations to apply
  - `"lowercase_keys"`: Convert keys to lowercase
  - `"remove_nulls"`: Remove null values
  - `"flatten"`: Flatten nested dictionaries

**Methods:**
- `register_transformer(name: str, transformer: Callable)`: Add custom transformer

**Example:**
```python
transformer = DataTransformerModule({
    "transformations": ["remove_nulls", "lowercase_keys"]
})
```

### RateLimiterModule

Controls request rates.

**Configuration:**
- `requests_per_second` (int): Maximum requests per second
- `burst_size` (int): Burst size for rate limiting

**Methods:**
- `get_stats()`: Get rate limiter statistics

**Example:**
```python
limiter = RateLimiterModule({
    "requests_per_second": 2,
    "burst_size": 5
})
```

## Integration Modules

### AutoBuilderIntegration

Integration with auto builder system.

**Configuration:**
- `endpoint` (str): Auto builder API endpoint
- `api_key` (str): API key for authentication
- `build_type` (str): Type of build to trigger

**Methods:**
- `trigger_build(data: Dict)`: Trigger a build

### FoundationIntegration

Integration with foundation system.

**Configuration:**
- `storage_path` (str): Path for data storage
- `database_url` (str): Database connection URL
- `schema_version` (str): Data schema version

**Methods:**
- `retrieve_data(query: Dict)`: Retrieve stored data

### TaxonomyIntegration

Integration with taxonomy system.

**Configuration:**
- `taxonomy_url` (str): Taxonomy API endpoint
- `default_categories` (List[str]): Default categories
- `auto_classify` (bool): Enable automatic classification

**Methods:**
- `add_category(data: Dict, category: str)`: Add category to data
- `get_categories()`: Get available categories

### GatewayIntegration

Integration with gateway system.

**Configuration:**
- `gateway_url` (str): Gateway API endpoint
- `routing_rules` (Dict): Routing rules configuration
- `retry_enabled` (bool): Enable retry on failure
- `max_retries` (int): Maximum retry attempts

**Methods:**
- `add_route(name: str, destination: str, conditions: Dict)`: Add routing rule

## Utility Functions

### config_loader

#### load_config(config_path: str) -> Dict[str, Any]

Load configuration from YAML file.

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- Dict[str, Any]: Configuration dictionary

**Raises:**
- FileNotFoundError: If config file doesn't exist
- yaml.YAMLError: If config file is invalid

#### save_config(config: Dict[str, Any], config_path: str) -> None

Save configuration to YAML file.

**Parameters:**
- `config` (Dict[str, Any]): Configuration to save
- `config_path` (str): Path to save configuration

### url_utils

#### normalize_url(url: str) -> str

Normalize a URL by removing fragments and standardizing format.

**Parameters:**
- `url` (str): URL to normalize

**Returns:**
- str: Normalized URL

#### is_valid_url(url: str) -> bool

Check if a URL is valid.

**Parameters:**
- `url` (str): URL to validate

**Returns:**
- bool: True if valid, False otherwise

#### get_domain(url: str) -> Optional[str]

Extract domain from a URL.

**Parameters:**
- `url` (str): URL to extract domain from

**Returns:**
- Optional[str]: Domain or None if invalid
