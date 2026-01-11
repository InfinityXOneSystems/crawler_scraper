import os

# Define the output directory for logs and results
OUTPUT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', 'crawler_scraper_output', 'raw'
    )
)
os.makedirs(OUTPUT_DIR, exist_ok=True)


CONFIGS = {
    "real_estate": {
        "user_agent": "InfinityRealEstateBot/1.0"
    },
    "finance": {
        "user_agent": "InfinityFinanceBot/1.0"
    },
    "generic": {
        "user_agent": "InfinityGenericBot/1.0"
    }
}

def get_config(industry: str) -> dict:
    return CONFIGS.get(industry, CONFIGS["generic"])
