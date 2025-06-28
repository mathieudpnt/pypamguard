# registry.py
# A module for registering the available modules (subclasses of PAMChunk)

from pypamguard.modules import ClickDetector, RWEdgeDetector
from pypamguard.generics import GenericModule

MODULES = {
    b"Click Detector": ClickDetector,
    b"Right Whale Edge Detector": RWEdgeDetector
}

def module_metadata(module):
    return {
        "name": module,
        "class": MODULES[module],
        "minimum_version": MODULES[module]._minimum_version,
        "maximum_version": MODULES[module]._maximum_version,
    }


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

    for module in MODULES:
        registry.register_module(module, MODULES[module])
