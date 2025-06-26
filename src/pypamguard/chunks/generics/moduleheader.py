from ..standard.chunkinfo import ChunkInfo
from utils.readers import *
from chunks.generics.chunk import GenericChunk
import io

class ModuleHeader(GenericChunk):
    
    def __init__(self):
        super().__init__()

    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo):
        super().process(data, chunk_info)

        self.version: int = NumericalBinaryReader(INTS.INT).process(data)
        self.binary_length: int = NumericalBinaryReader(INTS.INT).process(data)