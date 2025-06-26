from ..generics.module import GenericModule

from ..standard.fileheader import FileHeader
from ..generics.moduleheader import ModuleHeader
from ..standard.chunkinfo import ChunkInfo
from ..generics.modulefooter import GenericModuleFooter
from utils.readers import *
from filters import Filters

class ClickDetectorFooter(GenericModuleFooter):

    def __init__(self, file_header: FileHeader, module_header: ModuleHeader):
        super().__init__(file_header, module_header)

        self.types_count_length: int = None
        self.types_count: list[int] = None

    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        if self.binary_length > 0:
            self.types_count_length = NumericalBinaryReader(INTS.SHORT).process(data)
            self.types_count = NumericalBinaryReader(INTS.INT, shape = self.types_count_length).process(data)

class ClickDetector(GenericModule):

    _footer = ClickDetectorFooter

    def __init__(self, file_header: FileHeader, module_header: ModuleHeader):
        super().__init__(file_header, module_header)

        self.start_sample: int = None
        self.channel_map: Bitmap = None
        self.trigger_map: Bitmap = None
        self.type: int = None
        self.flags: Bitmap = None
        self.delays: float = None
        self.angles: float = None
        self.angle_errors: float = None
        self.duration: int = None
        self.wave: np.ndarray = None

    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo, pg_filters: Filters):
        super().process(data, chunk_info, pg_filters)

        # data_length should be INTS.INT but fsm this works
        data_length = NumericalBinaryReader(INTS.SHORT).process(data)

        if self._module_header.version <= 3:
            self.start_sample = NumericalBinaryReader(INTS.LONG).process(data)
            self.channel_map = BitmapBinaryReader(INTS.INT).process(data)

        self.trigger_map = BitmapBinaryReader(INTS.INT).process(data)
        self.type = NumericalBinaryReader(INTS.SHORT).process(data)
        self.flags = BitmapBinaryReader(INTS.INT).process(data)

        if self._module_header.version <= 3:
            n_delays = NumericalBinaryReader(INTS.SHORT).process(data)
            if n_delays: self.delays = NumericalBinaryReader(FLOATS.FLOAT).process(data)

        n_angles = NumericalBinaryReader(INTS.SHORT).process(data)
        if n_angles: self.angles = NumericalBinaryReader(FLOATS.FLOAT, shape=n_angles).process(data)
        
        n_angle_errors = NumericalBinaryReader(INTS.SHORT).process(data)
        if n_angle_errors: self.angle_errors = NumericalBinaryReader(FLOATS.FLOAT, shape=n_angle_errors).process(data)

        if self._module_header.version <= 3: self.duration = NumericalBinaryReader(INTS.USHORT).process(data)
        else: self.duration = self.sample_duration

        max_val = NumericalBinaryReader(FLOATS.FLOAT).process(data)

        def normalize_wave(x):
            result = x * max_val / 127
            return np.round(result, 4)

        self.wave = NumericalBinaryReader(INTS.CHAR, post_processor=normalize_wave, shape=(len(self.channel_map.get_set_bits()), self.duration)).process(data)
