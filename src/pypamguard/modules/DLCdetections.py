from pypamguard.standard import StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *

class DeepLearningClassifierDetections(StandardModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n_chan: np.int16 = None
        self.n_samps: np.int32 = None
        self.scale: np.float32 = None
        self.wave: np.ndarray[np.float32] = None

    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        data_length = br.bin_read(DTYPES.INT32)
        self.n_chan = br.bin_read(DTYPES.INT16)
        self.n_samps = br.bin_read(DTYPES.INT32)
        self.scale = br.bin_read((DTYPES.FLOAT32, lambda x: 1/x))
        self.wave = br.bin_read((DTYPES.INT8, lambda x: x/self.scale), shape=(self.n_chan, self.n_samps))