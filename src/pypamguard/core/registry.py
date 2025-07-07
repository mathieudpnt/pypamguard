# registry.py
# A module for registering the available modules (subclasses of PAMChunk)

from pypamguard.modules import *
from pypamguard.modules.ltsa import LTSA
from pypamguard.modules.ishmaeldetections import IshmaelDetections
from pypamguard.modules.DLCdetections import *
from pypamguard.modules.DLCmodels import DeelLearningClassifierModels
from pypamguard.generics import GenericModule
from pypamguard.core.exceptions import ModuleNotFoundException

class Module:
    def __init__(self, classes):
        self.classes = classes
    
    def get_class(self, stream_name):
        if type(self.classes) == dict: return self.classes[stream_name]
        else: return self.classes

aisprocessing_config = None

clickdetector_config = {
    "Clicks": ClickDetector,
    "Trigger Background": None,
}

clipgenerator_config = ClipGenerator

deeplearningclassifier_config = {
    "DL_detection": None,
    "DL detection": None,
    "DL_Model_Data": DeelLearningClassifierModels,
    "DL Model Data": DeelLearningClassifierModels,
}

dbht_config = None

difarprocessing_config = None

noisemonitor_config = None

noiseband_config = None

gpldetector_config = None

rwedgedetector_config = RWEdgeDetector

wmdetector_config = WhistleAndMoanDetector

ltsa_config = LTSA

ishmaeldetector_config = {
    "Ishmael Peak Data": None,
    "Ishmael Detections": IshmaelDetections,
}

ipimodule_config = None

geminithresholddetector_config = None

MODULES = {
    "AIS Processing": Module(aisprocessing_config),
    "Click Detector": Module(clickdetector_config),
    "SoundTrap Click Detector": Module(clickdetector_config),
    "Clip generator": Module(clipgenerator_config),
    "Deep Learning Classifier": Module(deeplearningclassifier_config),
    "DbHt": Module(dbht_config),
    "DIFAR Processing": Module(difarprocessing_config),
    "LTSA": Module(ltsa_config),
    "Noise Monitor": Module(noisemonitor_config),
    "Noise Band": Module(noiseband_config),
    "GPL Detector": Module(gpldetector_config),
    "RW Edge Detector": Module(rwedgedetector_config),
    "WhistlesMoans": Module(wmdetector_config),
    "Energy Sum Detector": Module(ishmaeldetector_config),
    "Spectrogram Correlation Detector": Module(ishmaeldetector_config),
    "Matched Filter Detector": Module(ishmaeldetector_config),
    "Ipi module": Module(ipimodule_config),
    "Gemini Threshold Detector": Module(geminithresholddetector_config),
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

    def register_module(self, module_name: str, module_class: Module):
        """Register a new module (must be a subclass of GenericModule)"""
        if module_name in self.modules:
            raise ValueError(f"Module {module_name} is already registered. Deregister module first by calling `deregister_module('{module_name}')`.")
        self.modules[module_name] = module_class
    
    def deregister_module(self, module_name: str) -> int:
        """Deregister a module. Returns the number of modules deregistered (either 0 or 1)"""
        if module_name in self.modules:
            del self.modules[module_name]
            return 1
        return 0
    
    def get_module(self, module_name: str, module_stream) -> GenericModule:
        if module_name in self.modules and type(self.modules[module_name]) == Module:
            return self.modules[module_name].get_class(module_stream)
        raise ModuleNotFoundException(f"Module '{module_name}' is not registered.")

def register_preinstalled_modules(registry: ModuleRegistry):

    for module in MODULES:
        registry.register_module(module, MODULES[module])
