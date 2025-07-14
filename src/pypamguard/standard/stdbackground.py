from pypamguard.generics.genbackground import GenericBackground
from pypamguard.standard import StandardModuleHeader, StandardFileHeader, StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *
from pypamguard.core.filters import Filters
from pypamguard.standard.stddata import StandardDataMixin

class StandardBackground(GenericBackground, StandardDataMixin):
    def __init__(self, file_header, module_header, filters,  *args, **kwargs):
        super().__init__(file_header, module_header, filters, *args, **kwargs)
        self._initialize_stddata()
    
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        self._process_stddata(br, chunk_info)
