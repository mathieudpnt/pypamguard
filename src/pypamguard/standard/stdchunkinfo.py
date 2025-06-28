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
        """Skips the current chunk in the binary file."""
        data.seek(self.next_chunk, io.SEEK_SET)

    @property
    def next_chunk(self) -> int:
        """Position of the next chunk in the binary file."""
        return self._start + self.length
