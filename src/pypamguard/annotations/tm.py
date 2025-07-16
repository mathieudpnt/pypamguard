from pypamguard.core.serializable import Serializable
from pypamguard.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers_new import *

class TMAnnotation(GenericAnnotation):

    class Location(Serializable):
        def __init__(self):
            self.latitude = None
            self.longitude = None
            self.height = None
            self.error = None

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        self.model = br.string_read()
        self.n_locations = br.bin_read(DTYPES.INT16)
        self.hydrophones = br.bin_read(DTYPES.UINT32)
        self.loc = np.ndarray(self.n_locations, type=self.Location)
        for i in range(self.n_locations):
            loc = self.Location()
            loc.latitude = br.bin_read(DTYPES.FLOAT64)
            loc.longitude = br.bin_read(DTYPES.FLOAT64)
            loc.height = br.bin_read(DTYPES.FLOAT32)
            loc.error = br.string_read()
            self.loc[i] = loc
