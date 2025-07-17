from pypamguard.core.serializable import Serializable
from pypamguard.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers import *

class RWUDPAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.label = br.string_read()
        self.method = br.string_read()
        self.score = br.bin_read(DTYPES.FLOAT32)
        