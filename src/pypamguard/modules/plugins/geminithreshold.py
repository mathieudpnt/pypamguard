from pypamguard.standard.stdmodule import StandardModule
from pypamguard.core.readers_new import *

class GeminiThresholdDetector(StandardModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n_points: np.int32 = None
        self.n_sonar: np.int8 = None
        self.sonar_ids: np.ndarray[np.int16] = None
        self.straight_length: np.float32 = None
        self.wobbly_length: np.float32 = None
        self.mean_occupancy: np.float32 = None
        self.time_millis: np.ndarray[np.int64] = None
        self.sonar_id: np.ndarray[np.int16] = None
        self.min_bearing: np.ndarray[np.float32] = None
        self.max_bearing: np.ndarray[np.float32] = None
        self.peak_bearing: np.ndarray[np.float32] = None
        self.min_range: np.ndarray[np.float32] = None
        self.max_range: np.ndarray[np.float32] = None
        self.peak_range: np.ndarray[np.float32] = None
        self.obj_size: np.ndarray[np.float32] = None
        self.occupancy: np.ndarray[np.float32] = None
        self.ave_value: np.ndarray[np.int16] = None
        self.tot_value: np.ndarray[np.int32] = None
        self.max_value: np.ndarray[np.int16] = None
        self.dates: np.ndarray[datetime.datetime] = None
    
    def _process(self, br, chunk_info):
        super()._process(br, chunk_info)
        self.n_points = br.bin_read(DTYPES.INT32)
        self.n_sonar = br.bin_read(DTYPES.INT8)
        self.sonar_ids = br.bin_read(DTYPES.INT16, shape=(self.n_sonar,))
        self.straight_length, self.wobbly_length, self.mean_occupancy = br.bin_read([DTYPES.FLOAT32, DTYPES.FLOAT32, DTYPES.FLOAT32])
        (
            self.time_millis,
            self.sonar_id,
            self.min_bearing,
            self.max_bearing,
            self.peak_bearing,
            self.min_range,
            self.max_range,
            self.peak_range,
            self.obj_size,
            self.occupancy,
            self.ave_value,
            self.tot_value,
            self.max_value,
        ) = br.bin_read([
            DTYPES.INT64,
            DTYPES.INT16,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.FLOAT32,
            DTYPES.INT16,
            DTYPES.INT32,
            DTYPES.INT16,
        ])
        self.dates = [BinaryReader.millis_to_timestamp(x) for x in self.millis]
