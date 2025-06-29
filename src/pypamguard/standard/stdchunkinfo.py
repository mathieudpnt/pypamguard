from pypamguard.base import BaseChunk
from pypamguard.core.readers import *
from pypamguard.generics import GenericChunkInfo
from pypamguard.utils.constants import IdentifierType
from pypamguard.core.exceptions import CriticalException, FileCorruptedException

class StandardChunkInfo(GenericChunkInfo):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length: int = None
        self.identifier: int = None

    def process(self, data):
        self._start = data.tell()
        self.length: int = NumericalBinaryReader(INTS.INT, var_name='length').process(data)
        self.identifier: int = NumericalBinaryReader(INTS.INT, var_name='identifier').process(data)
        if self.length < 0 or (self.identifier < 0 and self.identifier not in IdentifierType):
            raise FileCorruptedException(data)

    def skip(self, data: io.BufferedReader):
        """Skips the current chunk in the binary file."""
        data.seek(self.next_chunk, io.SEEK_SET)

    @property
    def next_chunk(self) -> int:
        """Position of the next chunk in the binary file."""
        return self._start + self.length
