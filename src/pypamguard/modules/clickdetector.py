from pypamguard.standard import StandardModule, StandardModuleFooter

from pypamguard.core.readers_new import *

class ClickDetectorFooter(StandardModuleFooter):

    def __init__(self, file_header, module_header):
        super().__init__(file_header, module_header)

        self.types_count_length: int = None
        self.types_count: list[int] = None

    def process(self, br, chunk_info):
        super().process(br, chunk_info)

        if self.binary_length > 0:
            self.types_count_length = br.read_numeric(DTYPES.INT16)
            if self.types_count_length > 0: self.types_count = br.read_numeric(DTYPES.INT32, shape=self.types_count_length)
            else: self.types_count = []

class ClickDetector(StandardModule):

    _minimum_version = 2
    _footer = ClickDetectorFooter

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)

        self.start_sample: int = None
        self.channel_map: Bitmap = None
        self.trigger_map: Bitmap = None
        self.type: int = None
        self.flags: Bitmap = None
        self.delays: float = None
        self.angles: np.ndarray = np.array([])
        self.angle_errors: np.ndarray = np.array([])
        self.duration: int = None
        self.wave: np.ndarray = None

    def process(self, br, chunk_info):
        super().process(br, chunk_info)

        # data_length should be INTS.INT but fsm this works
        data_length = br.read_numeric(DTYPES.INT32)

        if self._module_header.version <= 3:
            self.start_sample, self.channel_map = br.read_numeric([DTYPES.INT64, DTYPES.INT32])

        self.n_chan = len(self.channel_map.get_set_bits())

        self.trigger_map, self.type = br.read_numeric([DTYPES.INT32, DTYPES.INT16])
        self.flags = br.read_bitmap(DTYPES.INT32)

        if self._module_header.version <= 3:
            n_delays = br.read_numeric(DTYPES.INT16)
            if n_delays: self.delays = br.read_numeric(DTYPES.FLOAT32, shape=n_delays)

        n_angles = br.read_numeric(DTYPES.INT16)
        if n_angles: self.angles = br.read_numeric(DTYPES.FLOAT32, shape=n_delays)
        
        n_angle_errors = br.read_numeric(DTYPES.INT16)
        if n_angle_errors: self.angle_errors = br.read_numeric(DTYPES.FLOAT32, shape=n_angle_errors)

        if self._module_header.version <= 3: self.duration = br.read_numeric(DTYPES.UINT16)
        else: self.duration = self.sample_duration

        max_val = br.read_numeric(DTYPES.FLOAT32)

        def normalize_wave(x):
            return np.round(x * max_val / 127, 4)

        self.wave = br.read_numeric((DTYPES.INT8, normalize_wave), shape=(self.n_chan, self.duration))
