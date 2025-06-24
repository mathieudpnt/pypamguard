# Base class for PAMGuard modules

from field_types import *
from .basechunk import BaseChunk

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

class GenericModule(BaseChunk):

    millis: int
    flags: Bitmap
    time_ns: int
    channel_map: int
    uid: int
    start_sample: int
    sample_duration: int
    frequency_limits: int
    millis_duration: int
    time_delay: int
    has_binary_annotations: bool
    has_sequence_map: bool
    has_noise: bool
    has_signal: bool
    has_signal_excess: bool

    def __init__(self, data):
        self.millis = IntegerType(INTS.LONG).process(data)
        self.flags = BitmapType(INTS.SHORT, DATA_FLAG_FIELDS).process(data)
        set_flags = self.flags.get_set_bits()

        if "TIMENANOSECONDS" in set_flags:
            self.time_ns = IntegerType(INTS.LONG).process(data)
        
        if "CHANNELMAP" in set_flags:
            self.channel_map = BitmapType(INTS.INT).process(data)
        
        if "UID" in set_flags:
            self.uid = IntegerType(INTS.INT).process(data)
        
        if "STARTSAMPLE" in set_flags:
            self.start_sample = IntegerType(INTS.INT).process(data)
        
        if "SAMPLEDURATION" in set_flags:
            self.sample_duration = IntegerType(INTS.INT).process(data)
        
        if "FREQUENCYLIMITS" in set_flags:
            self.frequency_limits = IntegerType(INTS.INT).process(data)
        
        if "MILLISDURATION" in set_flags:
            self.millis_duration = IntegerType(INTS.INT).process(data)
        
        if "TIMEDELAYSECONDS" in set_flags:
            self.time_delay = IntegerType(INTS.INT).process(data)
        
        if "HASSEQUENCEMAP" in set_flags:
            self.has_sequence_map = IntegerType(INTS.SHORT).process(data)

        if "HASNOISE" in set_flags:
            self.has_noise = IntegerType(INTS.SHORT).process(data)

        if "HASSIGNAL" in set_flags:
            self.has_signal = IntegerType(INTS.SHORT).process(data)

        if "HASSIGNALEXCESS" in set_flags:
            self.has_signal_excess = IntegerType(INTS.SHORT).process(data)

        if "HASBINARYANNOTATIONS" in set_flags:
            self.has_binary_annotations = IntegerType(INTS.SHORT).process(data)
