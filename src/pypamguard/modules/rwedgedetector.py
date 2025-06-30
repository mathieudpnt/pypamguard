from pypamguard.standard import StandardModule
from ..core.readers import *

class RWEdgeDetector(StandardModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)

        self.sound_type: int = None
        self.signal: float = None
        self.noise: float = None
        self.n_slices: int = None

        self.slice_list: list[int] = []
        self.low_freq: list[int] = []
        self.peak_freq: list[int] = []
        self.high_freq: list[int] = []
        self.peak_amp: list[int] = []
    
    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        self.sound_type = NumericalBinaryReader(INTS.SHORT, var_name='sound_type').process(data)
        self.signal = NumericalBinaryReader(FLOATS.FLOAT, var_name='signal').process(data)
        self.noise = NumericalBinaryReader(FLOATS.FLOAT, var_name='noise').process(data)
        NumericalBinaryReader(INTS.INT).process(data)
        self.n_slices = NumericalBinaryReader(INTS.SHORT, var_name='n_slices').process(data)
        for _ in range(self.n_slices):
            self.slice_list.append(NumericalBinaryReader(INTS.SHORT, var_name='slice_list').process(data))
            self.low_freq.append(NumericalBinaryReader(INTS.SHORT, var_name='low_freq').process(data))
            self.peak_freq.append(NumericalBinaryReader(INTS.SHORT, var_name='peak_freq').process(data))
            self.high_freq.append(NumericalBinaryReader(INTS.SHORT, var_name='high_freq').process(data))
            self.peak_amp.append(NumericalBinaryReader(FLOATS.FLOAT, var_name='peak_amp').process(data))
        
