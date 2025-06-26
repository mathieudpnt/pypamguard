from ..generics.module import GenericModule
from ..standard.fileheader import FileHeader
from ..generics.moduleheader import ModuleHeader
from ..standard.chunkinfo import ChunkInfo
from utils.readers import *


class RWEdgeDetector(GenericModule):

    def __init__(self, data, data_header: ChunkInfo, file_header: FileHeader, module_header: ModuleHeader):
        super().__init__(data)
