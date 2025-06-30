from pypamguard.standard import StandardModule, StandardModuleFooter
from pypamguard.core.readers import *

class ClickDetectorFooter(StandardModuleFooter):

    def __init__(self, file_header, module_header):
        super().__init__(file_header, module_header)

        self.types_count_length: int = None
        self.types_count: list[int] = None

    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        if self.binary_length > 0:
            self.types_count_length = NumericalBinaryReader(INTS.SHORT).process(data)
            if self.types_count_length > 0: self.types_count = NumericalBinaryReader(INTS.INT, shape = self.types_count_length).process(data)
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

    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        # data_length should be INTS.INT but fsm this works
        data_length = NumericalBinaryReader(INTS.INT, var_name='data_length').process(data)

        if self._module_header.version <= 3:
            self.start_sample = NumericalBinaryReader(INTS.LONG, var_name='start_sample').process(data)
            self.channel_map = BitmapBinaryReader(INTS.INT, var_name='channel_map').process(data)

        self.n_chan = len(self.channel_map.get_set_bits())

        self.trigger_map = BitmapBinaryReader(INTS.INT, var_name='trigger_map').process(data)
        self.type = NumericalBinaryReader(INTS.SHORT, var_name='type').process(data)
        self.flags = BitmapBinaryReader(INTS.INT, var_name='flags').process(data)

        if self._module_header.version <= 3:
            n_delays = NumericalBinaryReader(INTS.SHORT, var_name='n_delays').process(data)
            if n_delays: self.delays = NumericalBinaryReader(FLOATS.FLOAT, var_name='delays').process(data)

        n_angles = NumericalBinaryReader(INTS.SHORT, var_name='n_angles').process(data)
        if n_angles: self.angles = NumericalBinaryReader(FLOATS.FLOAT, shape=n_angles, var_name='angles').process(data)
        
        n_angle_errors = NumericalBinaryReader(INTS.SHORT, var_name='n_angle_errors').process(data)
        if n_angle_errors: self.angle_errors = NumericalBinaryReader(FLOATS.FLOAT, shape=n_angle_errors, var_name='angle_errors').process(data)

        if self._module_header.version <= 3: self.duration = NumericalBinaryReader(INTS.USHORT, var_name='duration').process(data)
        else: self.duration = self.sample_duration

        max_val = NumericalBinaryReader(FLOATS.FLOAT, var_name='max_val').process(data)

        def normalize_wave(x):
            result = x * max_val / 127
            return np.round(result, 4)

        self.wave = NumericalBinaryReader(INTS.CHAR, post_processor=normalize_wave, shape=(len(self.channel_map.get_set_bits()), self.duration), var_name='wave').process(data)
