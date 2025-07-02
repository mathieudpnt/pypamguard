import io

from . import StandardChunkInfo
from pypamguard.generics import GenericFileHeader, GenericFileFooter
from pypamguard.core.readers_new import *

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

    def process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier

        self.n_objects = br.read_numeric(DTYPES.INT32)
        self.data_date_raw, self.data_date = br.read_timestamp()
        self.analysis_date_raw, self.analysis_date = br.read_timestamp()
        self.end_sample = br.read_numeric(DTYPES.INT64)
        if self._file_header.file_format >= 3:
            self.lowest_uid = br.read_numeric(DTYPES.INT64)
            self.highest_uid = br.read_numeric(DTYPES.INT64)
        self.file_length = br.read_numeric(DTYPES.INT64)
        self.end_reason = br.read_numeric(DTYPES.INT32)