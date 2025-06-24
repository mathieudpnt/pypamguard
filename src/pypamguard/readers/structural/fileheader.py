from ..basechunk import BaseChunk
from ..genericmodule import GenericModule
from .header import HeaderChunk
from field_types import *

class FileHeader(BaseChunk):

    file_format: int
    pamguard: str
    version: str
    branch: str
    data_date: str
    analysis_date: str
    start_sample: int
    module_type: str
    module_name: str
    stream_name: str
    extra_info_len: int

    def __init__(self, data):
        super().__init__(data)

        self.file_format = IntegerType(INTS.INT).process(data)
        self.pamguard = StringNType(12).process(data)
        self.version = StringType().process(data)
        self.branch = StringType().process(data)
        self.data_date = DateType().process(data)
        self.analysis_date = DateType().process(data)
        self.start_sample = IntegerType(INTS.LONG).process(data)
        self.module_type = StringType().process(data)
        self.module_name = StringType().process(data)
        self.stream_name = StringType().process(data)
        self.extra_info_len = IntegerType(INTS.INT).process(data)
