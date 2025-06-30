# field_types.py
# Classes that represent different types of fields in a PAMGuard file

import struct
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import io
import datetime

from pypamguard.utils.bitmap import Bitmap
from pypamguard.utils.constants import BYTE_ORDERS
from pypamguard.logger import logger

class TypeFormat():
    def __init__(self, formatter: str, size: int):
        self.formatter = formatter
        self.size = size

class DTYPES(Enum):
    CHAR = TypeFormat("b",1)
    UCHAR = TypeFormat("B",1)
    SHORT = TypeFormat("h",2)
    USHORT = TypeFormat("H",2)
    INT = TypeFormat("i",4)
    UINT = TypeFormat("I",4)
    LONG = TypeFormat("q",8)
    ULONG = TypeFormat("Q",8)
    FLOAT = TypeFormat("f",4)
    DOUBLE = TypeFormat("d",8)
    STRING = TypeFormat("s",1)

class INTS(Enum):
    CHAR = TypeFormat("b",1)
    UCHAR = TypeFormat("B",1)
    SHORT = TypeFormat("h",2)
    USHORT = TypeFormat("H",2)
    INT = TypeFormat("i",4)
    UINT = TypeFormat("I",4)
    LONG = TypeFormat("q",8)
    ULONG = TypeFormat("Q",8)

class FLOATS(Enum):
    FLOAT = TypeFormat("f",4)
    DOUBLE = TypeFormat("d",8)


from abc import ABC, abstractmethod
import io

class BinaryReader(ABC):

    def __init__(self, as_helper = False, var_name = None):
        """
        A class that represents a field in a PAMGuard Binary File. This class is used
        to define a data type (during construction) and then read the data from a binary
        file (using the `process()` method).
        """
        self.as_helper = as_helper
        self.var_name=var_name
    
    @abstractmethod
    def process(self, data: io.BufferedReader, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN):
        """
        Reads data from a binary file (as configured in the constructor).
        """
        if not isinstance(data, io.BufferedReader): raise ValueError(f"data must be of type io.BufferedReader (got {type(data)}).")
        if order not in list(BYTE_ORDERS): raise ValueError(f"order must be one of: {list(BYTE_ORDERS)} (got {str(order)}).")

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def print(self, result = None):
        logger.debug(f"{self.var_name} = {result}")

class NumericalBinaryReader(BinaryReader):

    def __init__(self, format: INTS | FLOATS, shape: tuple[int] = None, post_processor: callable = None, as_helper = False, var_name = None):
        """
        A reader class for numerical data types in a PAMGuard Binary File. The constructure will configure the reader
        to read data of a specific format and optionally apply a post processor.

        @param format: The format of the data to read (see constants.INTS and constants.FLOATS).
        @param post_processor: A function that will be applied to the data read from the file (must be callable).
        @param shape: The shape of the data to be read. For example `shape=(5)` means that 5 values will be read and returned
                    as a 1D numpy array. `shape=(2,40)` means that 2 rows, with 40 elements  each will be read and returned as
                    a 2D numpy array (an entire row is read from the binary file before starting on the next one). If shape is
                    left as `None` then a single primitive (`int` or `float`) will be returned.
        """
        if post_processor and not callable(post_processor): raise ValueError("post_processor must be callable (try a lambda function).")
        if format not in INTS and format not in FLOATS: raise ValueError(f"format must be one of: {list(INTS) + list(FLOATS)} (got {str(format)}).")
        if shape and not isinstance(shape, (int, tuple)): raise ValueError(f"shape must be of type tuple (got {type(shape)}).")

        self.shape = shape
        self.format = format
        self.post_processor = post_processor
        super().__init__(as_helper, var_name=var_name)

    def process(self, data, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN) -> int | float | np.ndarray:
        super().process(data, order) # type checking inputs
        byte_size = self.format.value.size * np.prod(self.shape) if self.shape else self.format.value.size
        result = np.frombuffer(data.read(byte_size), dtype= np.dtype(order.value + self.format.value.formatter))
        if self.shape: result = result.reshape(self.shape)
        if self.post_processor is not None: result = self.post_processor(result)
        result = result.item() if not self.shape else result
        self.print(result)
        return result

    def __str__(self):
        return f"{self.__class__.__name__}('shape'={self.shape}, 'format'={self.format}, 'post_processor'={self.post_processor})"

class StringNBinaryReader(BinaryReader):
    def __init__(self, length: int, post_processor: callable = None, as_helper = False, var_name = None):
        """
        A class that represents a string field in a PAM file.
        """
        if post_processor and not callable(post_processor): raise ValueError("post_processor must be callable (try a lambda function).")
        if not isinstance(length, int): raise ValueError(f"length must be of type int (got {type(length)}).")

        self.length = length
        self.post_processor = post_processor

        super().__init__(as_helper, var_name=var_name)
    
    def process(self, data, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN):
        super().process(data, order) # type checking inputs
        result = struct.unpack(order.value + f"{self.length}s", data.read(self.length))[0]
        if self.post_processor is not None: result = self.post_processor(result)
        self.print(result)
        return result.decode() if type(result) == bytes else result

class StringBinaryReader(BinaryReader):
    # TODO: change to inherit from StringNType
    def __init__(self, as_helper = False, var_name=None):
        """
        A class that represents a string field in a PAM file,
        where the length of the string is preceeded by a 16 bit integer.
        """
        self.length_type = NumericalBinaryReader(INTS.USHORT)
        super().__init__(as_helper, var_name=var_name)
    
    def process(self, data, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN):
        super().process(data, order)
        length = self.length_type.process(data)
        result = StringNBinaryReader(length, as_helper=True).process(data)
        self.print(result)
        return result.decode() if type(result) == bytes else result

class CustomBinaryReader(BinaryReader):
    def __init__(self, function, count, var_name=None):
        self.function = function
        self.count = count
        super().__init__(var_name=var_name)
    
    def process(self, data, order):
        super().process(data, order)
        return self.function(data, self.count)
    
class DateBinaryReader(BinaryReader):
    """Date in millis"""

    def __init__(self, as_helper = False, var_name=None):
        super().__init__(as_helper, var_name=var_name)

    def process(self, data):
        epoch_millis = NumericalBinaryReader(INTS.LONG, as_helper=True).process(data)
        result = datetime.datetime.fromtimestamp(epoch_millis / 1000, datetime.UTC)
        self.print(result)
        return result

class BitmapBinaryReader(BinaryReader):
    def __init__(self, format: INTS, labels = None, as_helper = False, var_name=None):
        super().__init__(as_helper, var_name=var_name)
        self.format = format
        self.labels = labels
        self.bm = Bitmap(format.value.size * 8, labels)
    
    def process(self, data):
        self.bm.bits = NumericalBinaryReader(self.format, as_helper=True).process(data)
        self.print(self.bm)
        return self.bm