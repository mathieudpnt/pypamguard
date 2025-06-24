from ..basechunk import BaseChunk
from field_types import *

class HeaderChunk(BaseChunk):

    length: int
    identifier: int

    def __init__(self, data):
        super().__init__(data)

        self.length = IntegerType(INTS.INT).process(data)
        self.identifier = IntegerType(INTS.INT).process(data)
