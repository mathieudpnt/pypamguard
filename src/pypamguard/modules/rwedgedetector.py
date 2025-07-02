from pypamguard.standard import StandardModule
from pypamguard.core.readers_new import DTYPES, BinaryReader
import numpy as np

class RWEdgeDetector(StandardModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)

        self.type: int = None
        self.signal: float = None
        self.noise: float = None
        self.n_slices: int = None
        self.slice_nums: np.ndarray = None
        self.lo_freqs: np.ndarray = None
        self.peak_freqs: np.ndarray = None
        self.hi_freqs: np.ndarray = None
        self.peak_amp: np.ndarray = None

    def process(self, br, chunk_info):
        super().process(br, chunk_info)

        data_length = br.read_numeric(DTYPES.INT32)
        self.type = br.read_numeric(DTYPES.INT16)
        self.signal = br.read_numeric(DTYPES.FLOAT32)
        self.noise = br.read_numeric(DTYPES.FLOAT32)
        self.n_slices = br.read_numeric(DTYPES.INT16)

        (self.slice_nums, self.lo_freqs, self.peak_freqs, self.hi_freqs, self.peak_amp) = br.read_numeric([DTYPES.INT16, DTYPES.INT16, DTYPES.INT16, DTYPES.INT16, DTYPES.FLOAT32], (self.n_slices,))
