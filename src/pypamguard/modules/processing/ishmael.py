from pypamguard.standard import StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *
from pypamguard.logger import logger

class IshmaelDetections(StandardModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        # Ishmael detections contain simply standard module data
        # NOTE: missing 20 bytes of data. Not accounted for in Matlab code.
        print(br.bin_read(DTYPES.FLOAT64)) # peak height
        print(br.bin_read(DTYPES.FLOAT64)) # time sample


class IshmaelData(StandardModule):
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        # Ishmael detections contain simply standard module data
        # NOTE: missing 20 bytes of data. Not accounted for in Matlab code.