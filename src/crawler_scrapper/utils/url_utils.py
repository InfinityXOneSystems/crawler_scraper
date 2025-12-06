"""URL utility functions."""

from urllib.parse import urlparse, urlunparse
from typing import Optional


def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing fragments and standardizing format.
    
    Args:
        url: URL to normalize
        
    Returns:
        Normalized URL
    """
    parsed = urlparse(url)
    # Remove fragment and rebuild URL
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        ""  # Remove fragment
    ))
    return normalized


def is_valid_url(url: str) -> bool:
    """
    Check if a URL is valid.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ["http", "https"], parsed.netloc])
    except Exception:
        return False


def get_domain(url: str) -> Optional[str]:
    """
    Extract domain from a URL.
    
    Args:
        url: URL to extract domain from
        
    Returns:
        Domain or None if invalid URL
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None
