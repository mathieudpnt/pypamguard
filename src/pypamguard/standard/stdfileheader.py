import io

from ..generics import GenericFileHeader
from pypamguard.core.readers_new import *

class StandardFileHeader(GenericFileHeader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def process(self, br: BinaryReader, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier

        self.file_format: int = br.read_numeric(DTYPES.INT32)
        self.pamguard: str = br.read_nstring(12)
        self.version: str = br.read_string()
        self.branch: str = br.read_string()
        self.data_date_raw, self.data_date = br.read_timestamp()
        self.analysis_date_raw, self.analysis_date = br.read_timestamp()
        self.start_sample: int = br.read_numeric(DTYPES.INT64)
        self.module_type: str = br.read_string()
        self.module_name: str = br.read_string()
        self.stream_name: str = br.read_string()
        self.extra_info_len: int = br.read_numeric(DTYPES.INT32)