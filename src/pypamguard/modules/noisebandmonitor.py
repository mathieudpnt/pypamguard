from pypamguard.standard import StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *

class NoiseBandMonitor(StandardModule):
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        data_length = br.bin_read(DTYPES.INT32)
        self.rms = br.bin_read((DTYPES.INT16, lambda x: x / 100))
        self.zero_peak = br.bin_read((DTYPES.INT16, lambda x: x / 100))
        self.peak_peak = br.bin_read((DTYPES.INT16, lambda x: x / 100))
        self.sel = br.bin_read((DTYPES.INT16, lambda x: x / 100))
        self.sel_secs = br.sel_secs = br.bin_read((DTYPES.INT16, lambda x: x / 100))
        