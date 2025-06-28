import io

from pypamguard.standard import StandardChunkInfo, StandardFileHeader, StandardFileFooter, StandardModuleHeader, StandardModuleFooter
from pypamguard.generics import GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter
from pypamguard.core.registry import ModuleRegistry
from pypamguard.core.modulewrapper import ModuleWrapper
from pypamguard.utils.constants import IdentifierType
from pypamguard.core.readers import BYTE_ORDERS
from pypamguard.core.filters import Filters, FILTER_POSITION, FilterMismatchException

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

        self.file_header: GenericFileHeader = StandardFileHeader()
        self.module_header: GenericModuleHeader = None
        self.module_footer: GenericModuleFooter = None
        self.file_footer: GenericFileFooter = StandardFileFooter(self.file_header)
        self.data_set: ModuleWrapper = None


    def __check_fully_read(self):
        return self.__data.tell() == self.file_size

    def load(self):
        
        prev = -1

        while True:
            

            # EOF checking is encouraged within modules. However this check
            # can prevent infinite loops and other errors.
            if self.__check_fully_read():
                break

            reconcile_chunk_length = True
            
            # Check that the pointer is moving forward, not back
            # No module must ever cause the pointer to go backwards
            if self.__data.tell() == prev:
                raise ValueError("File is not a valid PAMGuard binary file.")
            
            start_pos = self.__data.tell()

            chunk_info = StandardChunkInfo()
            chunk_info.process(self.__data)

            next_chunk = start_pos + chunk_info.length

            if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                self.file_header.process(self.__data, chunk_info)
                self.data_set = ModuleWrapper(self.__module_registry.get_module(self.file_header.module_name), self.file_header, self.filters)
                
                # NOTE this is a workaround for a bug in the PAMGuard file header writer
                # where the chunk length is not written correctly
                reconcile_chunk_length = False

            elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                try:
                    self.module_header = self.data_set.read_header(self.__data, chunk_info)
                except Exception as e:
                    print(f"Error reading module header: {e}")
                    chunk_info.skip(self.__data)
                    continue

            elif chunk_info.identifier >= 0:
                
                # If filter is set to terminate, skip the chunk
                if self.filters.position == FILTER_POSITION.STOP:
                    chunk_info.skip(self.__data)
                    continue
                
                try:
                    self.data_set.read_next(self.__data, chunk_info)
                # If filter mismatches, skip the chunk
                except FilterMismatchException:
                    chunk_info.skip(self.__data)
                # If an exception occurs, skip the chunk
                except Exception as e:
                    print(f"Error reading chunk: {e}")
                    chunk_info.skip(self.__data)
                    continue

            elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                try:
                    self.module_footer = self.data_set.read_footer(self.__data, chunk_info)
                except Exception as e:
                    print(f"Error reading module footer: {e}")
                    chunk_info.skip(self.__data)
                    continue
            
            elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                try:
                    self.file_footer = StandardFileFooter(self.file_header)
                    self.file_footer.process(self.__data, chunk_info)
                except Exception as e:
                    print(f"Error reading file footer: {e}")
                    chunk_info.skip(self.__data)
                    continue

            if reconcile_chunk_length:
                if self.__data.tell() != next_chunk:
                    print(f"Chunk length mismatch: {self.__data.tell()} != {next_chunk}")
                    self.__data.seek(next_chunk, io.SEEK_SET)
    
            
    def __str__(self):
        ret = f"PAMGuard Binary File (filename={self.filename}, size={self.file_size} bytes, order={self.order})\n\n"
        ret += f"{self.filters}\n"
        ret += f"File Header\n{self.file_header}\n\n"
        ret += f"Module Header\n{self.module_header}\n\n"
        ret += f"Module Footer\n{self.module_footer}\n\n"
        ret += f"File Footer\n{self.file_footer}\n\n"
        ret += f"Data Set: {self.data_set}"
        return ret