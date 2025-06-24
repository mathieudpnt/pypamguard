from ..basechunk import BaseChunk
from ..genericmodule import GenericModule
from ..structural.fileheader import FileHeader
from ..structural.moduleheader import ModuleHeader
from field_types import *

class RWEdgeDetector(GenericModule):

    def __init__(self, data, file_header: FileHeader, module_header: ModuleHeader):
        super().__init__(data)
