from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk

from .genfileheader import GenericFileHeader
from .genmoduleheader import GenericModuleHeader
from .genmodulefooter import GenericModuleFooter

from pypamguard.core.filters import FILTER_POSITION, Filters

class GenericModule(BaseChunk, ABC):

    _minimum_version = 0
    _maximum_version = None
    _footer = GenericModuleFooter # store the class of the footer

    def __init__(self, file_header: GenericFileHeader, module_header: GenericModuleHeader, filters: Filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_header = file_header
        self._module_header = module_header
        self._filters = filters
        
    @abstractmethod
    def process(self, data, chunk_info) -> FILTER_POSITION:
        raise NotImplementedError()
