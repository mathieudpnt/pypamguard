# registry.py
# A module for registering the available modules (subclasses of PAMChunk)

import importlib

from chunks.standard.chunkinfo import ChunkInfo
from chunks.generics.moduleheader import ModuleHeader
from chunks.standard.fileheader import FileHeader
from chunks.modules.clickdetector import ClickDetector
from chunks.modules.rwedgedetector import RWEdgeDetector
from chunks.generics.module import GenericModule
from chunks.generics.module import GenericModule

class ModuleRegistry:
    def __init__(self):
        self.modules = {}
        register_preinstalled_modules(self)

    def register_module(self, module_name: str, module_class: GenericModule):
        """Register a new module (must be a subclass of GenericModule)"""
        if module_name in self.modules:
            raise ValueError(f"Module {module_name} is already registered. Deregister module first by calling `deregister_module('{module_name}')`.")
        if not issubclass(module_class, GenericModule):
            raise ValueError(f"Module {module_name} must be a subclass of GenericModule.")
        self.modules[module_name] = module_class
    
    def deregister_module(self, module_name: str) -> int:
        """Deregister a module. Returns the number of modules deregistered (either 0 or 1)"""
        if module_name in self.modules:
            del self.modules[module_name]
            return 1
        return 0
    
    def get_module(self, module_name: str) -> GenericModule:
        if module_name in self.modules:
            return self.modules[module_name]
        return None

def register_preinstalled_modules(registry: ModuleRegistry):
    MODULES = [
        (b"Click Detector", ClickDetector),
        (b"Right Whale Edge Detector", RWEdgeDetector)
    ]

    for module in MODULES:
        registry.register_module(module[0], module[1])