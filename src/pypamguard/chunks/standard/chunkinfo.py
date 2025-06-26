from chunks.basechunk import BaseChunk
from utils.readers import *

class ChunkInfo(BaseChunk):
    
    def __init__(self):
        super().__init__()

        self.length: int = None
        self.identifier: int = None

    def process(self, data):
        super().process(data)

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