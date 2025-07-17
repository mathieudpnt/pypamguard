from pypamguard.generics import GenericAnnotation
from pypamguard.core.readers import *

class BeamFormerAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.hydrophones = br.bin_read(DTYPES.UINT32)
        self.array_type = br.bin_read(DTYPES.INT16)
        self.localisation_content = br.bin_read(DTYPES.UINT32)
        self.n_angles = br.bin_read(DTYPES.INT16)
        self.angles = br.bin_read(DTYPES.FLOAT32, shape=(self.n_angles,))
