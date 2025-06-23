from .basechunk import BaseChunk
from field import Field

from field_types import *

STRUCTURE = [
    Field("fileFormat", IntegerType(INTS.INT)),
    Field("pamguard", StringNType(12)),
    Field("version", StringType()),
    Field("branch", StringType()),
    Field("dataDate", DateType()),
    Field("analysisDate", DateType()),
    Field("startSample", IntegerType(INTS.LONG)),
    Field("moduleType", StringType()),
    Field("moduleName", StringType()),
    Field("streamName", StringType()),
    Field("extraInfoLen", IntegerType(INTS.INT)),
]

class HeaderChunk(BaseChunk):

    def __init__(self, data):
        super().__init__(data)
        for field in STRUCTURE:
            setattr(self, field.name, field.process(data))
            print(f"{field.name}: {getattr(self, field.name)}")
