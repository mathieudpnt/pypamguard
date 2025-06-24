from ..basechunk import BaseChunk
from .header import HeaderChunk
from field_types import *

class ModuleHeader(BaseChunk):

    version: int
    binary_length: int

    def __init__(self, data):
        super().__init__(data)

        self.version = IntegerType(INTS.INT).process(data)
        self.binary_length = IntegerType(INTS.INT).process(data)