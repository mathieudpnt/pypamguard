import io

from ..generics import GenericFileHeader
from pypamguard.core.readers import *

class StandardFileHeader(GenericFileHeader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_format: int = None
        self.pamguard: str = None
        self.version: str = None
        self.branch: str = None
        self.data_date: int = None
        self.analysis_date: int = None
        self.start_sample: int = None
        self.module_type: str = None
        self.module_name: str = None
        self.stream_name: str = None
        self.extra_info_len: int = None

    def process(self, data, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier

        self.file_format: int = NumericalBinaryReader(INTS.INT).process(data)
        self.pamguard: str = StringNBinaryReader(12).process(data)
        self.version: str = StringBinaryReader().process(data)
        self.branch: str = StringBinaryReader().process(data)
        self.data_date: int = DateBinaryReader().process(data)
        self.analysis_date: int = DateBinaryReader().process(data)
        self.start_sample: int = NumericalBinaryReader(INTS.LONG).process(data)
        self.module_type: str = StringBinaryReader().process(data)
        self.module_name: str = StringBinaryReader().process(data)
        self.stream_name: str = StringBinaryReader().process(data)
        self.extra_info_len: int = NumericalBinaryReader(INTS.INT).process(data)
