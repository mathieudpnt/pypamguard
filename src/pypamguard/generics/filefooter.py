from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk
from .fileheader import GenericFileHeader

class GenericFileFooter(BaseChunk, ABC):
    
    def __init__(self, file_header: GenericFileHeader):
        super().__init__()
        self._file_header = file_header

    @abstractmethod
    def process(self, data, chunk_info):
        raise NotImplementedError()
