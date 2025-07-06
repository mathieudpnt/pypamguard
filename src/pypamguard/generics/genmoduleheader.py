from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk
from .genfileheader import GenericFileHeader

class GenericModuleHeader(BaseChunk, ABC):
    
    def __init__(self, file_header: GenericFileHeader, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_header = file_header

        self.length: int = None
        self.identifier: int = None
