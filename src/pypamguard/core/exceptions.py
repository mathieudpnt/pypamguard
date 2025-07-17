import io
from pypamguard.chunks.generics import GenericChunkInfo
from pypamguard.chunks.base import BaseChunk
from pypamguard.core.readers import BinaryReader

class BinaryFileException(Exception):

    def __init__(self, br: BinaryReader):
        super().__init__()
        self.position = br.tell()

    def __str__(self):
        return f"{self.__class__.__name__}: at position {self.position} bytes"

class WarningException(BinaryFileException):
    
    def __init__(self, br: BinaryReader, chunk_info: GenericChunkInfo, chunk_obj: BaseChunk):
        super().__init__(br)
        self.chunk_info = chunk_info
        self.chunk_obj = chunk_obj

    def __str__(self):
        return f"{super().__str__()}, reading {self.chunk_obj.__class__}"


class ChunkLengthMismatch(WarningException):
    def __init__(self, br, chunk_info, chunk_obj):
        super().__init__(br, chunk_info, chunk_obj)
    
    def __str__(self):
        return super().__str__() + f", expected chunk length {self.chunk_info.length if self.chunk_info else 'unknown'} bytes, got {self.chunk_obj._measured_length + self.chunk_info._measured_length if self.chunk_obj else 'unknown'} bytes"

class CriticalException(BinaryFileException):
    pass

class ModuleNotFoundException(Exception):
    pass

class FileCorruptedException(CriticalException):
    pass

class StructuralException(FileCorruptedException):
    
    def __init__(self, file: io.BufferedReader, message=None):
        super().__init__(file)
        self.message = message
    
    def __str__(self):
        return f"{super().__str__()}, {self.message}"

class NoFileHeaderException(StructuralException):
    pass

class NoModuleHeaderException(StructuralException):
    pass

class NoModuleFooterException(StructuralException):
    pass

class NoFileFooterException(StructuralException):
    pass