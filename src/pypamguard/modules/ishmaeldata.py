from pypamguard.standard import StandardModule, StandardChunkInfo
from pypamguard.core.readers_new import *
from pypamguard.logger import logger

class IshmaelData(StandardModule):
    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        # Ishmael detections contain simply standard module data
        # NOTE: missing 20 bytes of data. Not accounted for in Matlab code.