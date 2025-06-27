import io

from pypamguard.generics import GenericChunkInfo, GenericFileHeader, GenericModuleFooter, GenericModuleHeader
from pypamguard.core.readers import *

class StandardModuleFooter(GenericModuleFooter):
    
    def __init__(self, file_header, module_header, *args, **kwargs):
        super().__init__(file_header, module_header, *args, **kwargs)

        self.binary_length: int = None
    
    def process(self, data, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier
        self.binary_length = NumericalBinaryReader(INTS.INT).process(data)
