# field_types.py
# Classes that represent different types of fields in a PAMGuard file

import struct
from enum import Enum
from abc import ABC, abstractmethod
from bitmap import Bitmap

class BYTE_ORDERS(Enum):
    NATIVE = "@"
    LITTLE_ENDIAN = "<"
    BIG_ENDIAN = ">"
    NETWORK = "!"

class TypeFormat():
    def __init__(self, formatter: str, size: int):
        self.formatter = formatter
        self.size = size

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

class Type(ABC):
    """
    A class that represents a field in a PAM file.
    """
    def __init__(self, *args, **kwargs):
        return

    @abstractmethod
    def process(self, data):
        raise NotImplementedError

class IntegerType(Type):
    def __init__(self, format: INTS):
        """
        A class that represents a integer field in a PAM file.
        """
        self.format = format
    
    def process(self, data):
        return struct.unpack(BYTE_ORDERS.NETWORK.value + self.format.value.formatter, data.read(self.format.value.size))[0]
        
class FloatType(Type):
    def __init__(self, format: FLOATS):
        """
        A class that represents a float field in a PAM file.
        """
        self.format = format
    
    def process(self, data):
        return struct.unpack(BYTE_ORDERS.NETWORK.value + self.format.value.formatter, data.read(self.format.value.size))

class StringNType(Type):
    def __init__(self, length: int):
        """
        A class that represents a string field in a PAM file.
        """
        self.length = length
    
    def process(self, data):
        return struct.unpack(BYTE_ORDERS.NETWORK.value + f"{self.length}s", data.read(self.length))[0]

class StringType(Type):
    # TODO: change to inherit from StringNType
    def __init__(self):
        """
        A class that represents a string field in a PAM file,
        where the length of the string is preceeded by a 16 bit integer.
        """
        self.length_type = IntegerType(INTS.USHORT)
    
    def process(self, data):
        length = self.length_type.process(data)
        return StringNType(length).process(data)

class CustomType(Type):
    def __init__(self, function, count):
        self.function = function
        self.count = count
    
    def process(self, data):
        return self.function(data, self.count)
    
class DateType(IntegerType):
    """Date in millis"""

    def __init__(self):
        super().__init__(INTS.LONG)

    def process(self, data):
        epoch_millis = super().process(data)
        return epoch_millis

class BitmapType(IntegerType):
    def __init__(self, format: INTS, labels = None):
        super().__init__(format)
        self.labels = labels
        self.bm = Bitmap(format.value.size * 8, labels)
    
    def process(self, data):
        self.bm.bits = super().process(data)
        return self.bm