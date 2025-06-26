from chunks.standard.fileheader import FileHeader
from chunks.generics.moduleheader import ModuleHeader
from chunks.standard.chunkinfo import ChunkInfo
from chunks.standard.filefooter import FileFooter
from chunks.generics.module import GenericModule
from data import DataSet
from registry import ModuleRegistry, register_preinstalled_modules
from constants import IdentifierType
from utils.readers import BYTE_ORDERS
import io
from filters import FilterBinaryFile, Filters, FILTER_POSITION, FilterStopSkipException

class PGBFile:
    
    def __init__(self, filename: str, data: io.BufferedReader, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, module_registry: ModuleRegistry = ModuleRegistry(), filters: Filters = Filters()):
        if not isinstance(data, io.BufferedReader): raise ValueError(f"data must be of type io.BufferedReader (got {type(data)}).")
        if order not in BYTE_ORDERS: raise ValueError(f"order must be one of: {list(BYTE_ORDERS)} (got {str(order)}).")
        if not isinstance(module_registry, ModuleRegistry): raise ValueError(f"module_registry must be of type registry.ModuleRegistry (got {type(module_registry)}).")

        self.__module_registry = module_registry
        self.__data = data
        
        self.file_size = data.seek(0, io.SEEK_END)
        self.__data.seek(0, io.SEEK_SET)
        
        self.filters = filters

        self.filename = filename
        self.order = order

        self.file_header: FileHeader = FileHeader()
        self.module_header: ModuleHeader = ModuleHeader()
        self.module_footer = None
        self.file_footer: FileFooter = None
        self.data_set: DataSet = None

    def check_fully_read(self):
        return self.__data.tell() == self.file_size

    def load(self):
        chunk_info = ChunkInfo()
        prev = self.__data.tell() - 1
        next_chunk = None

        while True:


            # EOF checking is encouraged within modules. However this check
            # can prevent infinite loops and other errors.
            if self.check_fully_read():
                break
            
            # Check that the pointer is moving forward, not back
            # No module must ever cause the pointer to go backwards
            if self.__data.tell() == prev:
                raise ValueError("File is not a valid PAMGuard binary file.")
            prev = self.__data.tell()

            chunk_info.process(self.__data)

            if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                self.file_header.process(self.__data, chunk_info)
                self.data_set = DataSet(self.__module_registry.get_module(self.file_header.module_name), self.file_header, self.module_header, self.filters)
                print(f"PAMFile.file_header: \n\t{'\n\t'.join([f'{key}: {value}' for key, value in self.file_header.signature().items()])}\n")

            elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                self.module_header.process(self.__data, chunk_info)
                print(f"PAMFile.module_header: \n\t{'\n\t'.join([f'{key}: {value}' for key, value in self.module_header.signature().items()])}\n")

            elif chunk_info.identifier >= 0:
                # If filter is set to terminate, skip the chunk
                if self.filters.position == FILTER_POSITION.STOP:
                    chunk_info.skip(self.__data)
                try:
                    self.data_set.read_next(self.__data, chunk_info)
                except FilterStopSkipException:
                    chunk_info.skip(self.__data)
                    continue
            
            elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                self.module_footer = self.data_set.read_footer(self.__data, chunk_info)
                print(f"PAMFile.module_footer: \n\t{'\n\t'.join([f'{key}: {value}' for key, value in self.module_footer.signature().items()])}\n")
                # print(str(self.module_footer))
            
            elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                self.file_footer = FileFooter(self.file_header)
                self.file_footer.process(self.__data, chunk_info)
                print(f"PAMFile.file_footer: \n\t{'\n\t'.join([f'{key}: {value}' for key, value in self.file_footer.signature().items()])}\n")

            else:
                break


        print(self.data_set)
        print(f"\t{'\n\t'.join(self.data_set.get_signature())}")
        # print(self.data_set.get(0))