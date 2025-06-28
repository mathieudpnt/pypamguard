import io
from pypamguard.generics import GenericChunkInfo, GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter, GenericModule
from pypamguard.core.filters import Filters

class ModuleWrapper():
    def __init__(self, module: GenericModule.__class__, file_header: GenericFileHeader, pg_filters: Filters = None):
        self.file_header: GenericFileHeader = file_header
        self.__module: GenericModule.__class__ = module
        self.module_header: GenericModuleHeader = None
        self.module_footer: GenericModuleFooter = None
        self.filters = pg_filters
        self.objects = []
    
    def __len__(self):
        return len(self.objects)

    def __getitem__(self, index):
        return self.objects[index]

    def read_next(self, data: io.BufferedReader, chunk_info: GenericChunkInfo):
        self.filters.position = None
        module_object = self.__module(self.file_header, self.module_header)
        module_object.process(data, chunk_info, self.filters)
        self.objects.append(module_object)
            

    def read_header(self, data: io.BufferedReader, chunk_info: GenericChunkInfo):
        self.module_header = self.__module._header(self.file_header)
        self.module_header.process(data, chunk_info)
        # if self.file_header.version < self.__module._minimum_version:
        #     raise ValueError(f"Module {self.__module.__name__} requires version {self.__module._minimum_version} or higher.")
        # if self.file_header.version > self.__module._maximum_version:
        #     raise ValueError(f"Module {self.__module.__name__} requires version {self.__module._maximum_version} or lower.")
        return self.module_header

    def read_footer(self, data: io.BufferedReader, chunk_info: GenericChunkInfo):
        self.module_footer = self.__module._footer(self.file_header, self.module_header)
        self.module_footer.process(data, chunk_info)
        return self.module_footer

    def get(self, index):
        return self.objects[index]

    def get_signature(self):
        return self.__module(self.file_header, self.module_header).get_attrs()

    def __str__(self):
        return (f"Module wrapper for {self.__module} with {len(self.objects)} objects")