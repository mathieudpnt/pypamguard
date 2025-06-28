import io

from . import StandardChunkInfo
from pypamguard.generics import GenericFileHeader, GenericFileFooter
from pypamguard.core.readers import *

class StandardFileFooter(GenericFileFooter):
    
    def __init__(self, file_header: GenericFileHeader):
        super().__init__(file_header)
        self.n_objects: int = None
        self.data_date: int = None
        self.analysis_date: int = None
        self.end_sample: int = None
        self.lowest_uid: int = None
        self.highest_uid: int = None
        self.file_length: int = None
        self.end_reason: int = None

    def process(self, data: io.BufferedReader, chunk_info: StandardChunkInfo):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier

        self.n_objects = NumericalBinaryReader(INTS.INT).process(data)
        self.data_date = DateBinaryReader().process(data)
        self.analysis_date = DateBinaryReader().process(data)
        self.end_sample = NumericalBinaryReader(INTS.LONG).process(data)
        if self._file_header.file_format >= 3:
            self.lowest_uid = NumericalBinaryReader(INTS.LONG).process(data)
            self.highest_uid = NumericalBinaryReader(INTS.LONG).process(data)
        self.file_length = NumericalBinaryReader(INTS.LONG).process(data)
        self.end_reason = NumericalBinaryReader(INTS.INT).process(data)