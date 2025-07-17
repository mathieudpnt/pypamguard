from pypamguard.core.serializable import Serializable
from pypamguard.chunks.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers import *

class ClickClsfrAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.n_classifications = br.bin_read(DTYPES.INT16)
        self.classify_set = br.bin_read(DTYPES.INT16, shape=(self.n_classifications,))