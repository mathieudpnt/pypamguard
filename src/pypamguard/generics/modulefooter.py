from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk

from .fileheader import GenericFileHeader
from .moduleheader import GenericModuleHeader

class GenericModuleFooter(BaseChunk, ABC):
    
    def __init__(self, file_header: GenericFileHeader, module_header: GenericModuleHeader, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_header = file_header
        self._module_header = module_header
    
    @abstractmethod
    def process(self, data, chunk_info):
        raise NotImplementedError()
