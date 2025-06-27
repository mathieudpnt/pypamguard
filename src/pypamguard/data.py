import io
from pypamguard.generics import GenericChunkInfo, GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter, GenericModule
from pypamguard.standard import StandardChunkInfo, StandardFileHeader, StandardFileFooter, StandardModuleHeader, StandardModuleFooter, StandardModule
from pypamguard.core.filters import Filters

class DataSet():
    def __init__(self, module: GenericModule.__class__, file_header: GenericFileHeader, module_header: GenericModuleHeader, pg_filters: Filters = None):
        self.file_header = file_header
        self.module_header = module_header
        self.module = module
        self.filters = pg_filters
        self.objects = []
    
    def read_next(self, data: io.BufferedReader, chunk_info: GenericChunkInfo):
        self.filters.position = None
        module_object = self.module(self.file_header, self.module_header)
        module_object.process(data, chunk_info, self.filters)
        self.objects.append(module_object)
            

    def read_footer(self, data: io.BufferedReader, chunk_info: GenericChunkInfo):
        footer_object = self.module._footer(self.file_header, self.module_header)
        footer_object.process(data, chunk_info)
        return footer_object

    def get(self, index):
        return self.objects[index]

    def get_signature(self):
        return self.module(self.file_header, self.module_header).get_attrs()

    def __str__(self):
        return (f"Module wrapper for {self.module.__name__} with {len(self.objects)} objects")