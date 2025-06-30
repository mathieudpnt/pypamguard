from pypamguard.standard import StandardModule, StandardModuleFooter, StandardModuleHeader
from pypamguard.core.readers import *
from numpy import ndarray
import numpy.typing as npt



class WhistleAndMoanDetectorHeader(StandardModuleHeader):
    def __init__(self, file_header):
        super().__init__(file_header)

        self.delay_scale: int = None
    
    def process(self, data, chunk_info):
        super().process(data, chunk_info)
        if self.binary_length != 0:
            self.delay_scale = NumericalBinaryReader(INTS.INT, var_name="delay_scale").process(data)

class WhistleAndMoanDetector(StandardModule):

    _header = WhistleAndMoanDetectorHeader

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)

        self.n_slices: int = None
        self.amplitude: float = None

        self.contour: ndarray
        self.contour_width: ndarray
        self.slice_numbers: ndarray
        self.n_peaks: ndarray
        self.peak_data: ndarray

        
    
    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        data_length = NumericalBinaryReader(INTS.INT, var_name="data_length").process(data)
        self.n_slices = NumericalBinaryReader(INTS.SHORT, var_name="n_slices").process(data)
        self.amplitude = NumericalBinaryReader(INTS.SHORT, var_name="amplitude").process(data) / 100

        self.slice_numbers = np.ndarray(shape=(self.n_slices,))
        self.n_peaks = np.ndarray(shape=(self.n_slices,))
        self.peak_data = np.empty(shape=(self.n_slices,), dtype=object)

        self.contour = np.ndarray(shape=(self.n_slices,))
        self.contour_width = np.ndarray(shape=(self.n_slices,))

        for i in range(self.n_slices):
            self.slice_numbers[i] = NumericalBinaryReader(INTS.INT, var_name=f"slice_number[{i}]").process(data)
            self.n_peaks[i] = NumericalBinaryReader(INTS.CHAR, var_name=f"n_peaks[{i}]").process(data)
            self.peak_data[i] = NumericalBinaryReader(INTS.SHORT, shape=(int(self.n_peaks[i]),4), var_name=f"peak_data[{i}]").process(data)
            self.contour[i] = self.peak_data[i][0][1]
            self.contour_width[i] = self.peak_data[i][0][2] - self.peak_data[i][0][0] + 1

        self.mean_width = self.contour_width.mean()