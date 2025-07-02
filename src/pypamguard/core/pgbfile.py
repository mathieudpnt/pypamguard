import io

from pypamguard.core.exceptions import BinaryFileException, WarningException, CriticalException, ChunkLengthMismatch, StructuralException
from pypamguard.base import BaseChunk
from pypamguard.standard import StandardChunkInfo, StandardFileHeader, StandardFileFooter, StandardModuleHeader, StandardModuleFooter
from pypamguard.generics import GenericChunkInfo, GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter, GenericModule
from pypamguard.core.registry import ModuleRegistry
from pypamguard.utils.constants import IdentifierType
from pypamguard.core.readers import BYTE_ORDERS
from pypamguard.core.filters import Filters, FILTER_POSITION, FilterMismatchException
from pypamguard.logger import logger
from pypamguard.core.serializable import Serializable
import threading
from pypamguard.core.readers_new import *
import concurrent.futures
import multiprocessing
import time, os
import sys
import tqdm

class Report(Serializable):
    warnings = []

    def add_warning(self, warning: Warning):
        logger.warning(str(warning))
        self.warnings.append(warning)
    
    def __str__(self):
        if len(self.warnings) == 0:
            return "No warnings"
        return f"{len(self.warnings)} warnings.\n"


def process_chunk(binary_reader: BinaryReader, chunk: GenericFileHeader | GenericModuleHeader | GenericModule | GenericModuleFooter | GenericFileFooter, chunk_info: StandardChunkInfo, reconcile_chunk_length: bool = True, i = None):
    # try:
    chunk.process(binary_reader, chunk_info)
    logger.debug(f"Processed chunk: {chunk.__class__} - {chunk}")
    # except FilterMismatchException as e:
    #     chunk_info.skip(self.__fp)
    #     logger.debug(f"Filter skipped chunk: {chunk.__class__} - {chunk}")
    #     return
    # except (WarningException) as e:
    #     self.__report.add_warning(e)
    #     chunk_info.skip(self.__fp)
    #     return
    logger.log_progress(binary_reader.file_offset)
    return chunk

class PGBFile(Serializable):
    """
    This class represents a PAMGuard Binary File
    """
    

    def __init__(self, path: str, fp: io.BufferedReader, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, module_registry: ModuleRegistry = ModuleRegistry(), filters: Filters = Filters()):
        """
        :param filename: The name of the file
        :param fp: The file pointer
        :param order: Override byte order of the file (optional)
        :param module_registry: Override the module registry (optional)
        :param filters: The filters (optional)
        """

        self.__path: str = path
        self.__filename = os.path.basename(self.__path)
        self.__fp: io.BufferedReader = fp
        self.__order: BYTE_ORDERS = order
        self.__module_registry: ModuleRegistry = module_registry
        self.__filters: Filters = filters
        self.__module_class: GenericModule # will be overriden by module registry
        self.__size: int = self.__get_size()

        self.__report: Report = Report()
        self.__file_header: GenericFileHeader = StandardFileHeader()
        self.__module_header: GenericModuleHeader = None
        self.__module_footer: GenericModuleFooter = None
        self.__file_footer: GenericFileFooter = StandardFileFooter(self.__file_header)
        self.__data: list[GenericModule] = []

    @property
    def size(self):
        return self.__size

    @property
    def file_header(self):
        return self.__file_header
    
    @property
    def module_header(self):
        return self.__module_header
    
    @property
    def module_footer(self):
        return self.__module_footer
    
    @property
    def file_footer(self):
        return self.__file_footer

    @property
    def filters(self):
        return self.__filters
    
    @property
    def module_class(self):
        return self.__module_class
    
    @property
    def order(self):
        return self.__order
    
    @property
    def path(self):
        return self.__path
    
    @property
    def module_registry(self):
        return self.__module_registry
    
    @property
    def data(self):
        return self.__data

    def __get_size(self):
        temp = self.__fp.tell()
        self.__fp.seek(0, io.SEEK_END)
        size = self.__fp.tell()
        self.__fp.seek(temp, io.SEEK_SET)
        return size
        
    def load(self):
        self.__fp.seek(0, io.SEEK_SET) # reset
        logger.start_progress_bar(self.__size, f"Processing", unit="KB", scale=1/1024, rounding=0)
        
        chunk_info = StandardChunkInfo()

        with multiprocessing.Pool(processes=20) as pool:
            futures = []
            i = 0
            while True:
                start_pos = self.__fp.tell()

                # EOF checking is encouraged within modules. However this check
                # can prevent infinite loops and other errors.
                if start_pos == self.__size:
                    break

                chunk_info.process(BinaryReader(self.__fp, 8))
                
                if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                    chunk_info.length = 107
                    binary_reader = BinaryReader(self.__fp, chunk_info.length - 8)
                    self.__file_header = process_chunk(binary_reader, self.__file_header, chunk_info, reconcile_chunk_length=False)
                    self.__module_class = self.__module_registry.get_module(self.__file_header.module_name)



                elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                    binary_reader = BinaryReader(self.__fp, chunk_info.length - 8)
                    if not self.__file_header: raise StructuralException(self.__fp, "File header not found before module header")
                    self.__module_header = process_chunk(binary_reader, self.__module_class._header(self.__file_header), chunk_info)


                elif chunk_info.identifier >= 0:
                    binary_reader = BinaryReader(self.__fp, chunk_info.length - 8)

                    if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before data")
                    
                    if self.__filters.position == FILTER_POSITION.STOP:
                        chunk_info.skip(self.__fp)
                        continue

                    args = (binary_reader, self.__module_class(self.__file_header, self.__module_header, self.__filters), chunk_info)
                    future = pool.apply_async(process_chunk, args)
                    i += 1
                    futures.append(future)

                elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                    binary_reader = BinaryReader(self.__fp, chunk_info.length - 8)
                    if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before module footer")
                    self.__module_footer = process_chunk(binary_reader, self.__module_class._footer(self.__file_header, self.__module_header), chunk_info)

                elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                    binary_reader = BinaryReader(self.__fp, chunk_info.length - 8)
                    if not self.__file_header: raise StructuralException(self.__fp, "File header not found before file footer")
                    self.__file_footer = process_chunk(binary_reader, self.__file_footer, chunk_info)

            for future in futures:
                chunk = future.get()
                if chunk: self.__data.append(chunk)

            logger.log_progress(self.__fp.tell())

        return chunk

    def to_json(self):
        return {
            "filters": self.filters.to_json(),
            "report": self.__report.to_json(),
            "file_header": self.__file_header.to_json(),
            "module_header": self.__module_header.to_json(),
            "module_footer": self.__module_footer.to_json(),
            "file_footer": self.__file_footer.to_json(),
            "data": [chunk.to_json() for chunk in self.__data],
        }

    def __str__(self):
        ret = f"PAMGuard Binary File (filename={self.__path}, size={self.size} bytes, order={self.__order})\n\n"
        ret += f"{self.__filters}\n"
        
        ret += f"{self.__report}"

        ret += f"File Header\n{self.__file_header}\n\n"
        ret += f"Module Header\n{self.__module_header}\n\n"
        ret += f"Module Footer\n{self.__module_footer}\n\n"
        ret += f"File Footer\n{self.__file_footer}\n\n"
        ret += f"Data Set: {len(self.__data)} objects\n"
        return ret