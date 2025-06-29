import io

from ..generics import GenericFileHeader
from pypamguard.core.readers import *

class StandardFileHeader(GenericFileHeader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def process(self, data, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier

        self.file_format: int = NumericalBinaryReader(INTS.INT, var_name='file_format').process(data)
        self.pamguard: str = StringNBinaryReader(12, var_name='pamguard').process(data)
        self.version: str = StringBinaryReader(var_name='version').process(data)
        self.branch: str = StringBinaryReader(var_name='branch').process(data)
        self.data_date: int = DateBinaryReader(var_name='data_date').process(data)
        self.analysis_date: int = DateBinaryReader(var_name='analysis_date').process(data)
        self.start_sample: int = NumericalBinaryReader(INTS.LONG, var_name='start_sample').process(data)
        self.module_type: str = StringBinaryReader(var_name='module_type').process(data)
        self.module_name: str = StringBinaryReader(var_name='module_name').process(data)
        self.stream_name: str = StringBinaryReader(var_name='stream_name').process(data)
        self.extra_info_len: int = NumericalBinaryReader(INTS.INT, var_name='extra_info_len').process(data)