from pypamguard.standard import StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *

class DeelLearningClassifierModels(StandardModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        data_length = br.bin_read(DTYPES.INT32)
        self.type = br.bin_read(DTYPES.INT8)
        self.is_binary = br.bin_read(DTYPES.UINT8) # logical
        self.scale = br.bin_read(DTYPES.FLOAT32)
        self.n_species = br.bin_read(DTYPES.INT16)
        self.predictions = br.bin_read((DTYPES.INT16, lambda x: x / self.scale), shape=(self.n_species,))
        self.n_class = br.bin_read(DTYPES.INT16)
        br.bin_read(DTYPES.INT16, shape=(self.n_class,))