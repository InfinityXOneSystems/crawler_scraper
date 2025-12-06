"""Data transformation module."""

from typing import Any, Dict, Optional, Callable
from ..core.base_module import BaseModule


class DataTransformerModule(BaseModule):
    """
    Module for transforming crawled/scraped data.
    
    Applies transformations to prepare data for different systems.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize data transformer.
        
        Args:
            config: Configuration including transformation rules
        """
        super().__init__(config)
        self.transformations = self.config.get("transformations", [])
        self.custom_transformers: Dict[str, Callable] = {}
    
    def initialize(self) -> bool:
        """Initialize the transformer."""
        return True
    
    def execute(self, data: Any) -> Any:
        """
        Transform data.
        
        Args:
            data: Data to transform
            
        Returns:
            Transformed data
        """
        if not isinstance(data, dict):
            return data
        
        result = data.copy()
        
        # Apply built-in transformations
        for transform in self.transformations:
            if transform == "lowercase_keys":
                result = self._lowercase_keys(result)
            elif transform == "remove_nulls":
                result = self._remove_nulls(result)
            elif transform == "flatten":
                result = self._flatten(result)
        
        # Apply custom transformations
        for name, transformer in self.custom_transformers.items():
            result = transformer(result)
        
        return result
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        pass
    
    def _lowercase_keys(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert all keys to lowercase."""
        return {k.lower(): v for k, v in data.items()}
    
    def _remove_nulls(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove null/None values."""
        return {k: v for k, v in data.items() if v is not None}
    
    def _flatten(self, data: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
        """Flatten nested dictionaries."""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def register_transformer(self, name: str, transformer: Callable) -> None:
        """
        Register a custom transformer function.
        
        Args:
            name: Name of the transformer
            transformer: Function that takes data and returns transformed data
        """
        self.custom_transformers[name] = transformer
