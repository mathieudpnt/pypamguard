from pypamguard.core.serializable import Serializable
from pypamguard.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers import *

class TBDLAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.n_angles = br.bin_read(DTYPES.INT16)
        self.angles = br.bin_read(DTYPES.FLOAT32, shape=(self.n_angles))
        self.n_errors = br.bin_read(DTYPES.INT16)
        self.errors = br.bin_read(DTYPES.FLOAT32, shape=(self.n_errors,))
        