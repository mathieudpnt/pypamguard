from chunks.generics.module import GenericModule
from chunks.standard.fileheader import FileHeader
from chunks.generics.moduleheader import ModuleHeader
from chunks.standard.chunkinfo import ChunkInfo
from filters import FilterBinaryFile, Filters, FILTER_POSITION, FilterStopSkipException

import io

class DataSet():
    def __init__(self, module: GenericModule.__class__, file_header: FileHeader, module_header: ModuleHeader, pg_filters: Filters = None):
        self.file_header = file_header
        self.module_header = module_header
        self.module = module
        self.filters = pg_filters
        self.objects = []
    
    def read_next(self, data: io.BufferedReader, chunk_info: ChunkInfo):
        self.filters.position = None
        module_object = self.module(self.file_header, self.module_header)
        module_object.process(data, chunk_info, self.filters)
        self.objects.append(module_object)
            

    def read_footer(self, data: io.BufferedReader, chunk_info: ChunkInfo):
        footer_object = self.module._footer(self.file_header, self.module_header)
        footer_object.process(data, chunk_info)
        return footer_object

    def get(self, index):
        return self.objects[index]

    def get_signature(self):
        return self.module(self.file_header, self.module_header).get_attrs()

    def __str__(self):
        return (f"Module wrapper for {self.module.__name__} with {len(self.objects)} objects")