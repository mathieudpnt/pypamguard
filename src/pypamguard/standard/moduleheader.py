from pypamguard.generics import GenericModuleHeader
from pypamguard.core.readers import *

class StandardModuleHeader(GenericModuleHeader):
    
    def __init__(self, file_header, *args, **kwargs):
        super().__init__(file_header, *args, **kwargs)

    def process(self, data, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier
        self.version: int = NumericalBinaryReader(INTS.INT).process(data)
        self.binary_length: int = NumericalBinaryReader(INTS.INT).process(data)
