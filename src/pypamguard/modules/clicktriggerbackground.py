from pypamguard.standard import StandardModule, StandardChunkInfo, StandardModuleHeader
from pypamguard.core.readers_new import *

class ClickTriggerBackgroundHeader(StandardModuleHeader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _process(self, br, chunk_info):
        super()._process(br, chunk_info)
        if self.binary_length != 0:
            self.channel_map = br.bitmap_read(DTYPES.INT32)
            self.n_chan = len(self.channel_map.get_set_bits())
            self.calibration = br.bin_read(DTYPES.FLOAT32, shape=(self.n_chan,))


class ClickTriggerBackground(StandardModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        data_length = br.bin_read(DTYPES.INT32)
        self.scale = br.bin_read(DTYPES.FLOAT32)
        self.raw_levels = br.bin_read((DTYPES.INT16, lambda x: x / self.scale), shape=(self.n_chan,))
        
