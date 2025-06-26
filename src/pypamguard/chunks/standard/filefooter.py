import io
from chunks.standard.chunkinfo import ChunkInfo
from chunks.standard.fileheader import FileHeader
from chunks.generics.chunk import GenericChunk
from utils.readers import *

class FileFooter(GenericChunk):
    def __init__(self, file_header: FileHeader):
        super().__init__()

        self.__file_header = file_header

        self.n_objects: int = None
        self.data_date: int = None
        self.analysis_date: int = None
        self.end_sample: int = None
        self.lowest_uid: int = None
        self.highest_uid: int = None
        self.file_length: int = None
        self.end_reason: int = None

    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo):
        super().process(data, chunk_info)

        self.n_objects = NumericalBinaryReader(INTS.INT).process(data)
        self.data_date = DateBinaryReader().process(data)
        self.analysis_date = DateBinaryReader().process(data)
        self.end_sample = NumericalBinaryReader(INTS.LONG).process(data)
        if self.__file_header.file_format >= 3:
            self.lowest_uid = NumericalBinaryReader(INTS.LONG).process(data)
            self.highest_uid = NumericalBinaryReader(INTS.LONG).process(data)
        self.file_length = NumericalBinaryReader(INTS.LONG).process(data)
        self.end_reason = NumericalBinaryReader(INTS.INT).process(data)