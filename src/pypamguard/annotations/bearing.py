from pypamguard.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers_new import *

class BearingAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.algorithm_name = br.string_read()
        self.hydrophones = br.bin_read(DTYPES.UINT32)
        self.array_type = br.bin_read(DTYPES.INT16)
        self.localisation_content = br.bin_read(DTYPES.UINT32)
        self.n_angles = br.bin_read(DTYPES.INT16)
        self.angles = br.bin_read(DTYPES.FLOAT32, shape=(self.n_angles,))
        self.n_errors = br.bin_read(DTYPES.INT16)
        self.errors = br.bin_read(DTYPES.FLOAT32, shape=(self.n_errors))
        if self.annotation_version >= 2:
            self.n_ang = br.bin_read(DTYPES.INT16)
            self.ang = br.bin_read(DTYPES.FLOAT32, shape=(self.n_ang,))
            