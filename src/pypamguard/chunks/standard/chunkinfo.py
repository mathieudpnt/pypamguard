from chunks.basechunk import BaseChunk
from utils.readers import *

class ChunkInfo(BaseChunk):
    
    def __init__(self):
        super().__init__()

    def process(self, data):
        super().process(data)

        self.length: int = NumericalBinaryReader(INTS.INT).process(data)
        self.identifier: int = NumericalBinaryReader(INTS.INT).process(data)
