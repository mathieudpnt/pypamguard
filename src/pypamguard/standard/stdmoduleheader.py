from pypamguard.generics import GenericModuleHeader
from pypamguard.core.readers_new import *

class StandardModuleHeader(GenericModuleHeader):
    
    def __init__(self, file_header, *args, **kwargs):
        super().__init__(file_header, *args, **kwargs)

        self.length: int = None
        self.identifier: int = None
        self.version: str = None
        self.binary_length: int = None

    def process(self, br: BinaryReader, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier
        self.version: int = br.read_numeric(DTYPES.INT32)
        self.binary_length: int = br.read_numeric(DTYPES.INT32)
