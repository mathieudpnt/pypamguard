# Base class for PAMGuard modules

from chunks.generics.moduleheader import ModuleHeader
from chunks.standard.fileheader import FileHeader
from chunks.standard.chunkinfo import ChunkInfo
from chunks.generics.modulefooter import GenericModuleFooter
from chunks.generics.chunk import GenericChunk
from utils.readers import *
import annotations
import io
import datetime
from filters import FilterBinaryFile, FilterDate, FILTER_POSITION, Filters


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

class GenericModule(GenericChunk):

    _footer = GenericModuleFooter

    def __init__(self, file_header: FileHeader, module_header: ModuleHeader):
        if not isinstance(file_header, FileHeader): raise ValueError(f"file_header must be of type FileHeader (got {type(file_header)}).")
        if not isinstance(module_header, ModuleHeader): raise ValueError(f"module_header must be of type ModuleHeader (got {type(module_header)}).")

        self._file_header = file_header
        self._module_header = module_header

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

    def process(self, data: io.BufferedReader, chunk_info: ChunkInfo, pg_filters: Filters) -> FILTER_POSITION:
        if not isinstance(chunk_info, ChunkInfo): raise ValueError(f"chunk_info must be of type HeaderChunk (got {type(chunk_info)}).")
        super().process(data, chunk_info)

        self.millis = NumericalBinaryReader(INTS.LONG).process(data)
        
        self.date = datetime.datetime.fromtimestamp(self.millis / 1000, datetime.UTC)
        pg_filters.filter('daterange', self.date)

        self.flag_bitmap = BitmapBinaryReader(INTS.SHORT, DATA_FLAG_FIELDS).process(data)
        set_flags = self.flag_bitmap.get_set_bits()
        
        if "TIMENANOSECONDS" in set_flags:
            self.time_ns = NumericalBinaryReader(INTS.LONG).process(data)
        
        if "CHANNELMAP" in set_flags:
            self.channel_map = BitmapBinaryReader(INTS.INT).process(data)
        
        if "UID" in set_flags:
            self.uid = NumericalBinaryReader(INTS.LONG).process(data)
            pg_filters.filter('uidrange', self.uid)
            pg_filters.filter('uidlist', self.uid)
        
        if "STARTSAMPLE" in set_flags:
            self.start_sample = NumericalBinaryReader(INTS.LONG).process(data)
        
        if "SAMPLEDURATION" in set_flags:
            self.sample_duration = NumericalBinaryReader(INTS.INT).process(data)
        
        if "FREQUENCYLIMITS" in set_flags:
            self.freq_limits = [
                NumericalBinaryReader(FLOATS.FLOAT).process(data), NumericalBinaryReader(FLOATS.FLOAT).process(data)
            ]

        if "MILLISDURATION" in set_flags:
            self.millis_duration = NumericalBinaryReader(FLOATS.FLOAT).process(data)
        
        if "TIMEDELAYSECONDS" in set_flags:
            self.time_delays = []
            num_time_delays = NumericalBinaryReader(INTS.SHORT).process(data)
            for i in range(num_time_delays):
                self.time_delays.append(NumericalBinaryReader(FLOATS.FLOAT).process(data))

        if "HASSEQUENCEMAP" in set_flags:
            self.sequence_map = NumericalBinaryReader(INTS.INT).process(data)

        if "HASNOISE" in set_flags:
            self.noise = NumericalBinaryReader(FLOATS.FLOAT).process(data)

        if "HASSIGNAL" in set_flags:
            self.signal = NumericalBinaryReader(FLOATS.FLOAT).process(data)

        if "HASSIGNALEXCESS" in set_flags:
            self.signal_excess = NumericalBinaryReader(FLOATS.FLOAT).process(data)

        # NOT COMPLETED YET
        if "HASBINARYANNOTATIONS" in set_flags:
            annotations_length = NumericalBinaryReader(INTS.SHORT).process(data)
            n_annotations = NumericalBinaryReader(INTS.SHORT).process(data)
            for i in range(n_annotations):
                annotation_length = NumericalBinaryReader(INTS.SHORT).process(data) - INTS.SHORT.value.size
                annotation_id = StringType().process(data)
                annotation_version = NumericalBinaryReader(INTS.SHORT).process(data)

                if annotation_id == "Beer":
                    annotations.read_beam_former_annotation(self, data)
                
                elif annotation_id == "Bearing":
                    annotations.read_bearing_annotation(self, data, annotation_version)
        else:
            self.annotations = []