"""Module manager for loading and managing crawler/scraper modules."""

import importlib
import inspect
from typing import Any, Dict, List, Optional, Type
from pathlib import Path

from .base_module import BaseModule


class ModuleManager:
    """
    Manager for dynamically loading and managing modules.
    
    This allows integration with external systems like auto builder,
    foundation, taxonomy, gateway, etc.
    """
    
    def __init__(self):
        """Initialize the module manager."""
        self.modules: Dict[str, BaseModule] = {}
        self.module_configs: Dict[str, Dict[str, Any]] = {}
    
    def register_module(
        self,
        name: str,
        module: BaseModule,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a module with the manager.
        
        Args:
            name: Name to register the module under
            module: Module instance to register
            config: Optional configuration for the module
        """
        self.modules[name] = module
        if config:
            self.module_configs[name] = config
        
        # Initialize the module
        if module.enabled:
            module.initialize()
    
    def unregister_module(self, name: str) -> None:
        """
        Unregister and cleanup a module.
        
        Args:
            name: Name of the module to unregister
        """
        if name in self.modules:
            self.modules[name].cleanup()
            del self.modules[name]
        if name in self.module_configs:
            del self.module_configs[name]
    
    def get_module(self, name: str) -> Optional[BaseModule]:
        """
        Get a registered module by name.
        
        Args:
            name: Name of the module
            
        Returns:
            Module instance or None if not found
        """
        return self.modules.get(name)
    
    def list_modules(self) -> List[str]:
        """
        List all registered module names.
        
        Returns:
            List of module names
        """
        return list(self.modules.keys())
    
    def execute_module(self, name: str, data: Any) -> Any:
        """
        Execute a specific module.
        
        Args:
            name: Name of the module to execute
            data: Input data for the module
            
        Returns:
            Output from the module
            
        Raises:
            ValueError: If module not found or not enabled
        """
        module = self.modules.get(name)
        if not module:
            raise ValueError(f"Module '{name}' not found")
        
        if not module.enabled:
            raise ValueError(f"Module '{name}' is not enabled")
        
        return module.execute(data)
    
    def execute_pipeline(self, module_names: List[str], data: Any) -> Any:
        """
        Execute a pipeline of modules in sequence.
        
        Args:
            module_names: List of module names to execute in order
            data: Initial input data
            
        Returns:
            Final output after all modules have processed
        """
        result = data
        for name in module_names:
            result = self.execute_module(name, result)
        return result
    
    def load_module_from_path(
        self,
        name: str,
        module_path: str,
        class_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Dynamically load a module from a file path.
        
        Args:
            name: Name to register the module under
            module_path: Python module path (e.g., 'mymodule.submodule')
            class_name: Name of the class to instantiate
            config: Optional configuration for the module
            
        Raises:
            ImportError: If module cannot be imported
            ValueError: If class is not a BaseModule subclass
        """
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            raise ImportError(f"Module not found: {module_path}") from e
        except Exception as e:
            raise ImportError(f"Failed to import module {module_path}: {e}") from e
        
        try:
            module_class = getattr(module, class_name)
        except AttributeError as e:
            raise ImportError(f"Class '{class_name}' not found in module {module_path}") from e
        
        if not inspect.isclass(module_class) or not issubclass(module_class, BaseModule):
            raise ValueError(f"{class_name} is not a valid BaseModule subclass")
        
        try:
            instance = module_class(config)
            self.register_module(name, instance, config)
        except Exception as e:
            raise ImportError(f"Failed to instantiate {class_name}: {e}") from e
    
    def get_all_module_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered modules.
        
        Returns:
            Dictionary mapping module names to their info
        """
        return {name: module.get_info() for name, module in self.modules.items()}
    
    def cleanup_all(self) -> None:
        """Cleanup all registered modules."""
        for module in self.modules.values():
            module.cleanup()
        self.modules.clear()
        self.module_configs.clear()
