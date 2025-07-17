from pypamguard.chunks.generics.genbackground import GenericBackground
from pypamguard.chunks.standard import StandardModuleHeader, StandardFileHeader, StandardModule, StandardChunkInfo
from pypamguard.core.readers import *
from pypamguard.core.filters import Filters
from pypamguard.chunks.standard.stddata import StandardDataMixin

class StandardBackground(GenericBackground, StandardDataMixin):
    def __init__(self, file_header, module_header, filters,  *args, **kwargs):
        super().__init__(file_header, module_header, filters, *args, **kwargs)
        self._initialize_stddata()
    
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        self._process_stddata(br, chunk_info)
