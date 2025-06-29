import io
from pypamguard.generics import GenericChunkInfo
from pypamguard.base import BaseChunk


class BinaryFileException(Exception):

    def __init__(self, file: io.BufferedReader):
        super().__init__()
        self.position = file.tell()


    def __str__(self):
        return f"{self.__class__.__name__}: at position {self.position} bytes"

class WarningException(BinaryFileException):
    
    def __init__(self, file, chunk_info: GenericChunkInfo = None, chunk: BaseChunk = None):
        super().__init__(file)
        self.chunk_info = chunk_info
        self.chunk = chunk

    def __str__(self):
        return f"{super().__str__()}, reading {self.chunk.__class__}"


class ChunkLengthMismatch(WarningException):
    def __init__(self, file, chunk_info = None, chunk = None):
        super().__init__(file, chunk_info, chunk)
    
    def __str__(self):
        return super().__str__() + f", expected position {self.chunk_info.next_chunk if self.chunk_info else 'unknown'} bytes"

class CriticalException(BinaryFileException):
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