import datetime

from pypamguard.generics import GenericModule, GenericModuleFooter
from .stdmodulefooter import StandardModuleFooter
from .stdmoduleheader import StandardModuleHeader
from pypamguard.core.readers_new import *
from pypamguard.core.exceptions import WarningException

DATA_FLAG_FIELDS = [
    "TIMEMILLISECONDS",
    "TIMENANOSECONDS",
    "CHANNELMAP",
    "UID",
    "STARTSAMPLE",
    "SAMPLEDURATION",
    "FREQUENCYLIMITS",
    "MILLISDURATION",
    "TIMEDELAYSECONDS",
    "HASBINARYANNOTATIONS",
    "HASSEQUENCEMAP",
    "HASNOISE",
    "HASSIGNAL",
    "HASSIGNALEXCESS"
]
import pickle

class StandardModule(GenericModule):

    _footer = StandardModuleFooter
    _header = StandardModuleHeader

    def pickleable(self):
        try:
            pickle.dumps(self)
        except pickle.PicklingError:
            return False
        return True

    def __init__(self, file_header, module_header, filters, *args, **kwargs):
        super().__init__(file_header, module_header, filters, *args, **kwargs)
        self.millis: int = None
        self.date: datetime.datetime = None
        self.flags: Bitmap = None
        self.time_ns: int = None
        self.channel_map: Bitmap = None
        self.uid: int = None
        self.start_sample: int = None
        self.sample_duration: int = None
        self.freq_limits: float = None
        self.millis_duration: float = None
        self.time_delays: list[float] = None
        self.sequence_map: float = None
        self.noise: float = None
        self.signal: float = None
        self.signal_excess: float = None

    def _process(self, br: BinaryReader, chunk_info):


        self.millis, self.date = br.timestamp_read()        
        self._filters.filter('daterange', self.date)

        self.flag_bitmap = br.bitmap_read(DTYPES.INT16, DATA_FLAG_FIELDS)
        set_flags = self.flag_bitmap.get_set_bits()
        
        if "TIMENANOSECONDS" in set_flags:
            self.time_ns = br.bin_read(DTYPES.INT64)
        
        if "CHANNELMAP" in set_flags:
            self.channel_map = br.bitmap_read(DTYPES.INT32)
        
        if "UID" in set_flags:
            self.uid = br.bin_read(DTYPES.INT64)
            self._filters.filter('uidrange', self.uid)
            self._filters.filter('uidlist', self.uid)
        
        if "STARTSAMPLE" in set_flags:
            self.start_sample = br.bin_read(DTYPES.INT64)
        
        if "SAMPLEDURATION" in set_flags:
            self.sample_duration = br.bin_read(DTYPES.INT32)
        
        if "FREQUENCYLIMITS" in set_flags:
            self.freq_limits = br.bin_read(DTYPES.FLOAT32, shape=(2,))

        if "MILLISDURATION" in set_flags:
            self.millis_duration = br.bin_read(DTYPES.FLOAT32)
        
        if "TIMEDELAYSECONDS" in set_flags:
            num_time_delays = br.bin_read(DTYPES.INT16)
            self.time_delays = br.bin_read(DTYPES.FLOAT32, shape=(num_time_delays,))

        if "HASSEQUENCEMAP" in set_flags:
            self.sequence_map = br.bin_read(DTYPES.INT32)

        if "HASNOISE" in set_flags:
            self.noise = br.bin_read(DTYPES.FLOAT32)

        if "HASSIGNAL" in set_flags:
            self.signal = br.bin_read(DTYPES.FLOAT32)

        if "HASSIGNALEXCESS" in set_flags:
            self.signal_excess = br.bin_read(DTYPES.FLOAT32)

        # NOT COMPLETED YET
        # if "HASBINARYANNOTATIONS" in set_flags:
        #     annotations_length = NumericalBinaryReader(INTS.SHORT).process(data)
        #     n_annotations = NumericalBinaryReader(INTS.SHORT).process(data)
        #     for i in range(n_annotations):
        #         annotation_length = NumericalBinaryReader(INTS.SHORT).process(data) - INTS.SHORT.value.size
        #         annotation_id = StringType().process(data)
        #         annotation_version = NumericalBinaryReader(INTS.SHORT).process(data)

        #         if annotation_id == "Beer":
        #             annotations.read_beam_former_annotation(self, data)
                
        #         elif annotation_id == "Bearing":
        #             annotations.read_bearing_annotation(self, data, annotation_version)
        # else:
        #     self.annotations = []

        self.annotations = []

        data_length = br.bin_read(DTYPES.INT32)
        if data_length <= 0: raise WarningException(br, chunk_info, self)