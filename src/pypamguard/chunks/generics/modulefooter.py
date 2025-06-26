from chunks.standard.fileheader import FileHeader
from chunks.generics.moduleheader import ModuleHeader
from chunks.standard.chunkinfo import ChunkInfo
from utils.readers import *
import io
from chunks.generics.chunk import GenericChunk


class GenericModuleFooter(GenericChunk):
    
    def __init__(self, file_header: FileHeader, module_header: ModuleHeader):
        super().__init__()

        self._file_header: FileHeader = file_header
        self._module_header: ModuleHeader = module_header

        self.binary_length: int = None
    
    @abstractmethod
    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo):
        super().process(data, chunk_info)

        self.binary_length = NumericalBinaryReader(INTS.INT).process(data)
