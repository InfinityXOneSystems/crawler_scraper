"""Base module interface for all crawler/scraper modules."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseModule(ABC):
    """
    Base class for all modules in the crawler/scraper system.
    
    This provides a standard interface for modules that can be loaded
    dynamically and integrated with other systems.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the module.
        
        Args:
            config: Optional configuration dictionary for the module
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self.enabled = self.config.get("enabled", True)
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the module.
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """
        Execute the module's main functionality.
        
        Args:
            data: Input data for the module
            
        Returns:
            Processed output data
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the module."""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the module.
        
        Returns:
            Dictionary containing module metadata
        """
        return {
            "name": self.name,
            "enabled": self.enabled,
            "config": self.config,
        }
