from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk

from .fileheader import GenericFileHeader
from .moduleheader import GenericModuleHeader
from .modulefooter import GenericModuleFooter

from pypamguard.core.filters import FILTER_POSITION, Filters

class GenericModule(BaseChunk, ABC):

    _footer = GenericModuleFooter # store the class of the footer

    def __init__(self, file_header: GenericFileHeader, module_header: GenericModuleHeader, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_header = file_header
        self._module_header = module_header

    @abstractmethod
    def process(self, data, chunk_info, pg_filters: Filters) -> FILTER_POSITION:
        raise NotImplementedError()
