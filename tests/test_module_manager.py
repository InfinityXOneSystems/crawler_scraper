"""Tests for the module manager."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler_scrapper.core import ModuleManager, BaseModule


class TestModule(BaseModule):
    """Test module for testing."""
    
    def initialize(self) -> bool:
        return True
    
    def execute(self, data):
        if isinstance(data, dict):
            data = data.copy()
            data["processed_by"] = self.name
        return data
    
    def cleanup(self):
        pass


def test_module_manager_initialization():
    """Test module manager initialization."""
    manager = ModuleManager()
    assert manager is not None
    assert len(manager.list_modules()) == 0


def test_register_module():
    """Test registering a module."""
    manager = ModuleManager()
    module = TestModule({"test_config": "value"})
    
    manager.register_module("test", module)
    
    assert "test" in manager.list_modules()
    assert manager.get_module("test") is not None


def test_unregister_module():
    """Test unregistering a module."""
    manager = ModuleManager()
    module = TestModule()
    
    manager.register_module("test", module)
    assert "test" in manager.list_modules()
    
    manager.unregister_module("test")
    assert "test" not in manager.list_modules()


def test_execute_module():
    """Test executing a module."""
    manager = ModuleManager()
    module = TestModule()
    
    manager.register_module("test", module)
    
    data = {"value": 123}
    result = manager.execute_module("test", data)
    
    assert result["value"] == 123
    assert result["processed_by"] == "TestModule"


def test_execute_pipeline():
    """Test executing a module pipeline."""
    manager = ModuleManager()
    
    # Register multiple modules
    manager.register_module("module1", TestModule())
    manager.register_module("module2", TestModule())
    
    data = {"value": 123}
    result = manager.execute_pipeline(["module1", "module2"], data)
    
    assert result["value"] == 123
    assert "processed_by" in result


def test_get_all_module_info():
    """Test getting all module information."""
    manager = ModuleManager()
    module = TestModule({"config_key": "config_value"})
    
    manager.register_module("test", module)
    
    info = manager.get_all_module_info()
    
    assert "test" in info
    assert info["test"]["name"] == "TestModule"
    assert info["test"]["enabled"] is True


def test_cleanup_all():
    """Test cleaning up all modules."""
    manager = ModuleManager()
    
    manager.register_module("test1", TestModule())
    manager.register_module("test2", TestModule())
    
    assert len(manager.list_modules()) == 2
    
    manager.cleanup_all()
    
    assert len(manager.list_modules()) == 0


if __name__ == "__main__":
    # Run tests
    test_module_manager_initialization()
    test_register_module()
    test_unregister_module()
    test_execute_module()
    test_execute_pipeline()
    test_get_all_module_info()
    test_cleanup_all()
    print("All tests passed!")
