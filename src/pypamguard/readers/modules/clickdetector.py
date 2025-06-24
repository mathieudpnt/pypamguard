from ..basechunk import BaseChunk
from ..genericmodule import GenericModule
from field_types import *

class ClickDetector(GenericModule):

    trigger_millis: int
    filename: str
    trigger_name: str
    trigger_uid: int

    def __init__(self, data):
        super().__init__(data)

        if self.length > 0:
            self.trigger_millis = IntegerType(INTS.LONG).process(data)
            self.filename = StringType().process(data)
            self.trigger_name = StringType().process(data)
            self.trigger_uid = IntegerType(INTS.LONG).process(data)


