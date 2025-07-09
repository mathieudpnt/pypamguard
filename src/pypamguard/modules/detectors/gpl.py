from pypamguard.standard import StandardModule
from pypamguard.core.readers_new import *

class GPLDetector(StandardModule):

    _minimum_version = 0 # As at 9 Jul 2025

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _process(self, br, chunk_info):
        super()._process(br, chunk_info)

        self.time_res = br.bin_read(DTYPES.FLOAT32)
        self.freq_res = br.bin_read(DTYPES.FLOAT32)
        self.area = br.bin_read(DTYPES.INT16)
        bit_depth = br.bin_read(DTYPES.INT8)
        if bit_depth == 8: p_type = DTYPES.UINT8
        else: p_type = DTYPES.UINT16
        # NOT COMPLETED