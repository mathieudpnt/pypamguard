from pypamguard.core.readers import *
from pypamguard.utils.bitmap import Bitmap
from numpy import ndarray
import io

class ReaderTest:
    def __init__(self, size, signed=True):
        self.size = size
        self.signed = signed
    
    def bytes2reader(self, data: bytes) -> io.BufferedReader:
        return io.BufferedReader(io.BytesIO(data))

    def value2bytes(self, d: int) -> bytes:
        return d.to_bytes(self.size, 'big', signed=self.signed)
    
    def get_data(self, value):
        return self.bytes2reader(self.value2bytes(value))

    def get_reader(self):
        raise NotImplementedError()

    def test_binary_reader(self, value):
        data = self.get_data(value)
        reader = self.get_reader()
        assert reader.process(data) == value

class NumericalReaderTest(ReaderTest):
    
    def __init__(self, reader_format: INTS | FLOATS, size, signed=True):
        self.reader_format = reader_format
        super().__init__(size, signed=signed)

    def get_reader(self):
        return NumericalBinaryReader(self.reader_format)
    
    def test_empty_buffer(self):
        data = self.bytes2reader(b'')
        reader = self.get_reader()
        assert reader.process(data) == 0
    
    def test_out_of_range_value():
        raise NotImplementedError

class IntegerReaderTest(NumericalReaderTest):
    def __init__(self):
        super().__init__(INTS.INT, 4)

    def test_min(self):
        data = self.bytes2reader(b'\x80\x00\x00\x00')
        assert self.get_reader().process(data) == -2147483648

    def test_max(self):
        data = self.bytes2reader(b'\x7F\xFF\xFF\xFF')
        assert self.get_reader().process(data) == 2147483647

class ShortReaderTest(NumericalReaderTest):
    def __init__(self):
        super().__init__(INTS.SHORT, 2)
    
class LongReaderTest(NumericalReaderTest):
    def __init__(self):
        super().__init__(INTS.LONG, 8)


class ShortReaderTest(ReaderTest):
    def __init__(self):
        super().__init__(2)
    
    def get_reader(self):
        return NumericalBinaryReader(INTS.SHORT)

VALUES = range(-100, 100, 10)

import pytest

@pytest.mark.parametrize("value", VALUES)
def test_int_binary_reader(value: int):
    test = IntegerReaderTest()
    test.test_binary_reader(value)
    test.test_min()
    test.test_max()

@pytest.mark.parametrize("value", VALUES)
def test_short_binary_reader(value: int):
    test = ShortReaderTest()
    test.test_binary_reader(value)


@pytest.mark.parametrize("value", VALUES)
def test_long_binary_reader(value: int):
    test = LongReaderTest()
    test.test_binary_reader(value)