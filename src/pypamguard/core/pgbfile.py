from contextlib import contextmanager
import io
import time

from pypamguard.core.exceptions import BinaryFileException, WarningException, CriticalException, ChunkLengthMismatch, StructuralException
from pypamguard.base import BaseChunk
from pypamguard.standard import StandardChunkInfo, StandardFileHeader, StandardFileFooter, StandardModuleHeader, StandardModuleFooter
from pypamguard.generics import GenericChunkInfo, GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter, GenericModule
from pypamguard.core.registry import ModuleRegistry
from pypamguard.utils.constants import IdentifierType
from pypamguard.utils.constants import BYTE_ORDERS
from pypamguard.core.filters import Filters, FILTER_POSITION, FilterMismatchException
from pypamguard.logger import logger, Verbosity
from pypamguard.core.serializable import Serializable
from pypamguard.core.readers import *
import multiprocessing
import os
import mmap

class Report(Serializable):
    warnings = []
    
    def __init__(self):
        self.warnings = []
    
    def add_warning(self, warning: WarningException):
        self.warnings.append(warning)
        logger.warning(warning)
    
    
    def __str__(self):
        if len(self.warnings) == 0:
            return "No warnings"
        return f"{len(self.warnings)} warnings.\n"

# Global report variable to be used for warning handling
report = Report()

@contextmanager
def mmap_file(file: int, access=mmap.ACCESS_READ, flags=mmap.MAP_SHARED):
    mm = mmap.mmap(file, 0, access=access, flags=flags)
    try:
        yield mm
    finally:
        mm.close()

def process_chunk1(file: int, pos: int, chunk: GenericFileHeader | GenericModuleHeader | GenericModule | GenericModuleFooter | GenericFileFooter, chunk_info: StandardChunkInfo, absorb_errors: bool = False):
    with mmap_file(file) as mm:
        return process_chunk(mm, pos, chunk, chunk_info, absorb_errors)


def create_mmap_and_process_chunk(chunk: GenericFileHeader | GenericModuleHeader | GenericModule | GenericModuleFooter | GenericFileFooter, chunk_info: StandardChunkInfo, fileno: int, pos: int, aborb_errors: bool = False):
    with mmap_file(fileno) as mm:
        return process_chunk(chunk, chunk_info, mm=mm, pos=pos, absorb_errors=aborb_errors)

def process_chunk(chunk, chunk_info, mm: mmap.mmap = None, pos: int = 0, absorb_errors: bool = False):
    mm.seek(pos)
    try:
        chunk.process(BinaryReader(mm), chunk_info)
        # Compare the actual chunk length to the expected chunk length
        if chunk._measured_length != chunk_info.length - chunk_info._measured_length:
            raise ChunkLengthMismatch(mm, chunk_info, chunk)
    except WarningException as e:
        # Warnings are added to a global report
        # Chunks with warnings are NOT SKIPPED
        report.add_warning(e)
    except FilterMismatchException as e:
        # Chunks with filter mismatches are SKIPPED
        return None
    except Exception as e:
        # Chunks with errors are SKIPPED
        # Errors will terminate the program if absorb_errors is False,
        # otherwise logged.
        if not absorb_errors: raise e
        logger.error(e)
        return None
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

        global report
        report = Report()
        self.__path: str = path
        self.__filename = os.path.basename(self.__path)
        self.__fp: io.BufferedReader = fp
        self.__order: BYTE_ORDERS = order
        self.__module_registry: ModuleRegistry = module_registry
        self.__filters: Filters = filters
        self.__module_class: GenericModule # will be overriden by module registry
        self.__size: int = self.__get_size()
        self.total_time: int = 0

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
        start_time = time.time()
        self.__fp.seek(0, io.SEEK_SET)
        with mmap_file(self.__fp.fileno()) as mm:
            # We use a pool to process chunks in parallel (asynchronously)
            # Note that headers and footers are still processed synchronously
            with multiprocessing.Pool(processes=1 if logger.verbosity == Verbosity.DEBUG else multiprocessing.cpu_count()) as pool:
                futures = []
                i = 0
                while True:
                    if mm.tell() == self.__size: break
                    chunk_info = StandardChunkInfo()
                    chunk_info.process(BinaryReader(mm))
                    chunk_pos = mm.tell()

                    if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                        self.__file_header = process_chunk(self.__file_header, chunk_info, mm=mm, pos=chunk_pos, absorb_errors=False)
                        self.__module_class = self.__module_registry.get_module(self.__file_header.module_type, self.__file_header.stream_name)

                    elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                        if not self.__file_header: raise StructuralException(self.__fp, "File header not found before module header")
                        self.__module_header = process_chunk(self.__module_class._header(self.__file_header), chunk_info, mm=mm, pos=chunk_pos, absorb_errors=False)

                    elif chunk_info.identifier >= 0:
                        logger.debug(f"Processing data chunk {i}")
                        i += 1
                        if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before data")
                        args = (self.__module_class(self.__file_header, self.__module_header, self.__filters), chunk_info, self.__fp.fileno(), chunk_pos, False)
                        futures.append(pool.apply_async(create_mmap_and_process_chunk, args))
                        # Because we are asynchronously processing chunks, we need to seek to the end of the chunk manually
                        mm.seek(chunk_pos + chunk_info.length - chunk_info._measured_length, io.SEEK_SET)

                    elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                        if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before module footer")
                        self.__module_footer = process_chunk(self.__module_class._footer(self.__file_header, self.__module_header), chunk_info, mm=mm, pos=chunk_pos)

                    elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                        if not self.__file_header: raise StructuralException(self.__fp, "File header not found before file footer")
                        self.__file_footer = process_chunk(self.__file_footer, chunk_info, mm=mm, pos=chunk_pos)

                    elif chunk_info.identifier == IdentifierType.FILE_BACKGROUND.value:
                        if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before data")
                        if self.__module_class._background is None: raise StructuralException(self.__fp, "Module class does not have a background specified")
                        args = (self.__module_class._background(self.__file_header, self.__module_header, self.__filters), chunk_info, self.__fp.fileno(), chunk_pos, False)
                        futures.append(pool.apply_async(create_mmap_and_process_chunk, args))
                        mm.seek(chunk_pos + chunk_info.length - chunk_info._measured_length, io.SEEK_SET)

                    else:
                        raise StructuralException(self.__fp, f"Unknown chunk identifier: {chunk_info.identifier}")

                for future in futures:
                    chunk = future.get()
                    if chunk and not chunk._filters.position in (FILTER_POSITION.SKIP, FILTER_POSITION.STOP): self.__data.append(chunk)
                    elif chunk and chunk._filters.position == FILTER_POSITION.STOP:
                        pool.terminate()
                        break

                pool.terminate()
                mm.close()
            
        self.total_time = time.time() - start_time

    def to_json(self):
        return {
            "filters": self.filters.to_json() if self.filters else None,
            "file_header": self.__file_header.to_json() if self.__file_header else None,
            "module_header": self.__module_header.to_json() if self.__module_header else None,
            "module_footer": self.__module_footer.to_json() if self.__module_footer else None,
            "file_footer": self.__file_footer.to_json() if self.__file_footer else None,
            "data": [chunk.to_json() for chunk in self.__data] if self.__data else None,
        }

    def __str__(self):
        ret = f"PAMGuard Binary File (filename={self.__path}, size={self.size} bytes, order={self.__order})\n\n"
        ret += f"{self.__filters}\n"
        ret += f"{report}"
        ret += f"File Header\n{self.__file_header}\n\n"
        ret += f"Module Header\n{self.__module_header}\n\n"
        ret += f"Module Footer\n{self.__module_footer}\n\n"
        ret += f"File Footer\n{self.__file_footer}\n\n"
        ret += f"Data Set: {len(self.__data)} objects\n"
        ret += f"Total time: {self.total_time:.2f} seconds\n"
        return ret