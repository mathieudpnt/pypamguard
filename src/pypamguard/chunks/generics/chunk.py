from chunks.standard.chunkinfo import ChunkInfo
from chunks.basechunk import BaseChunk
from abc import ABC, abstractmethod
import io

class GenericChunk(BaseChunk, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.length: int = None
        self.identifier: int = None

    @abstractmethod
    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo = None):
        super().process(data)

        if chunk_info:
            self.length = chunk_info.length
            self.identifier = chunk_info.identifier
