from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk

class GenericFileHeader(BaseChunk, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.length: int = None
        self.identifier: int = None

    @abstractmethod
    def process(self, data, chunk_info):
        raise NotImplementedError()
