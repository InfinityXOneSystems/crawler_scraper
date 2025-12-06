"""Data validation module."""

from typing import Any, Dict, List, Optional
from ..core.base_module import BaseModule


class DataValidatorModule(BaseModule):
    """
    Module for validating crawled/scraped data.
    
    Ensures data meets quality standards before passing to other systems.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize data validator.
        
        Args:
            config: Configuration including validation rules
        """
        super().__init__(config)
        self.required_fields = self.config.get("required_fields", [])
        self.min_content_length = self.config.get("min_content_length", 0)
        self.allowed_status_codes = self.config.get("allowed_status_codes", [200])
    
    def initialize(self) -> bool:
        """Initialize the validator."""
        return True
    
    def execute(self, data: Any) -> Any:
        """
        Validate data.
        
        Args:
            data: Data to validate
            
        Returns:
            Validated data with validation results
        """
        if not isinstance(data, dict):
            return {
                "valid": False,
                "errors": ["Data must be a dictionary"],
                "data": data,
            }
        
        errors = []
        warnings = []
        
        # Check required fields
        for field in self.required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check content length
        if "content" in data:
            content_length = len(str(data["content"]))
            if content_length < self.min_content_length:
                warnings.append(
                    f"Content length ({content_length}) below minimum ({self.min_content_length})"
                )
        
        # Check status code
        if "status_code" in data:
            if data["status_code"] not in self.allowed_status_codes:
                errors.append(f"Invalid status code: {data['status_code']}")
        
        result = data.copy()
        result["validation"] = {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
        
        return result
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        pass
