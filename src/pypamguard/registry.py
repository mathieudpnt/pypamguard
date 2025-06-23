# registry.py
# A module for registering the available modules (subclasses of PAMChunk)

import importlib
from .modules.base import BaseChunk

class ModuleRegistry:
    def __init__(self):
        self.modules = {}
    
    def register_module(self, module_name, module_class):
        """Register a new module (must be a subclass of BaseChunk)"""
        if module_name in self.modules:
            raise ValueError(f"Module {module_name} is already registered. Deregister module first by calling `deregister_module('{module_name}')`.")
        if not issubclass(module_class, BaseChunk):
            raise ValueError(f"Module {module_name} must be a subclass of BaseChunk.")
        self.modules[module_name] = module_class
    
    def deregister_module(self, module_name: str) -> int:
        """Deregister a module. Returns the number of modules deregistered (either 0 or 1)"""
        if module_name in self.modules:
            del self.modules[module_name]
            return 1
        return 0
    
    def get_module(self, module_name: str):
        if module_name in self.modules:
            return self.modules[module_name]
        return None
