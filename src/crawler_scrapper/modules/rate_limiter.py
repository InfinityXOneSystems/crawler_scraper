"""Rate limiting module."""

import time
from typing import Any, Dict, Optional
from ..core.base_module import BaseModule


class RateLimiterModule(BaseModule):
    """
    Module for rate limiting requests.
    
    Ensures crawling respects rate limits and doesn't overload servers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize rate limiter.
        
        Args:
            config: Configuration including rate limits
        """
        super().__init__(config)
        self.requests_per_second = self.config.get("requests_per_second", 1)
        self.burst_size = self.config.get("burst_size", 5)
        self.last_request_time = 0
        self.request_count = 0
    
    def initialize(self) -> bool:
        """Initialize the rate limiter."""
        self.last_request_time = time.time()
        self.request_count = 0
        return True
    
    def execute(self, data: Any) -> Any:
        """
        Apply rate limiting.
        
        Args:
            data: Data to pass through with rate limiting
            
        Returns:
            Data after applying rate limit delay
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        # Reset counter if enough time has passed
        if elapsed >= 1.0:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Check if we've exceeded the rate limit
        if self.request_count >= self.requests_per_second:
            sleep_time = 1.0 - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.request_count = 0
            self.last_request_time = time.time()
        
        self.request_count += 1
        
        # Add rate limit info to data
        if isinstance(data, dict):
            data = data.copy()
            data["rate_limit"] = {
                "requests_per_second": self.requests_per_second,
                "current_count": self.request_count,
            }
        
        return data
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get rate limiter statistics.
        
        Returns:
            Dictionary with rate limit stats
        """
        return {
            "requests_per_second": self.requests_per_second,
            "current_count": self.request_count,
            "last_request_time": self.last_request_time,
        }
