from pypamguard.base import BaseChunk
from pypamguard.core.readers import *
from pypamguard.generics import GenericChunkInfo

class StandardChunkInfo(GenericChunkInfo):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length: int = None
        self.identifier: int = None

    def process(self, data):
        self._start = data.tell()
        self.length: int = NumericalBinaryReader(INTS.INT).process(data)
        self.identifier: int = NumericalBinaryReader(INTS.INT).process(data)

    def skip(self, data: io.BufferedReader):
        if not self.length:
            raise ValueError("Chunk is not initialized. Call process() first.")
        data.seek(self._start + self.length, io.SEEK_SET)

    def get_next_chunk(self) -> int:
        """
        Returns the position of the next chunk in the file
        """
        return self._start + self.length
