import pytest, io
from pypamguard.core.readers import *
from pypamguard.utils.constants import BYTE_ORDERS
import struct
import numpy as np
import sys

import ctypes



ENDIANESS_VALUES = BYTE_ORDERS

INT8_MIN = np.iinfo(np.int8).min
INT8_MAX = np.iinfo(np.int8).max

INT16_MIN = np.iinfo(np.int16).min
INT16_MAX = np.iinfo(np.int16).max

INT32_MIN = np.iinfo(np.int32).min
INT32_MAX = np.iinfo(np.int32).max

INT64_MIN = np.iinfo(np.int64).min
INT64_MAX = np.iinfo(np.int64).max

UINT8_MAX = np.iinfo(np.uint8).max

UINT16_MAX = np.iinfo(np.uint16).max

UINT32_MAX = np.iinfo(np.uint32).max

UINT64_MAX = np.iinfo(np.uint64).max

FLOAT32_MIN = np.finfo(np.float32).min
FLOAT32_MAX = np.finfo(np.float32).max

FLOAT64_MIN = np.finfo(np.float64).min
FLOAT64_MAX = np.finfo(np.float64).max

def _factory_report():
    return Report()

def _factory_reader(buf: io.BytesIO, end: str = BYTE_ORDERS.BIG_ENDIAN) -> BinaryReader:
    """Create a factory BinaryReader object"""
    buf.seek(0)
    return BinaryReader(buf, _factory_report(), end)

@pytest.fixture
def buffer() -> io.BufferedIOBase:
    return io.BytesIO()

def _int8 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}b', v))

def _int16 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}h', v))

def _int32 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}i', v))

def _int64 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}q', v))

def _uint8 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}B', v))

def _uint16 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}H', v))

def _uint32 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}I', v))

def _uint64 (bf: io.BytesIO, v: int, end: str): 
    bf.write(struct.pack(f'{end.value}Q', v))

def _float32(bf: io.BytesIO, v: float, end: str):
    bf.write(struct.pack(f'{end.value}f', v))

def _float64(bf: io.BytesIO, v: float, end: str):
    bf.write(struct.pack(f'{end.value}d', v))

def _nstring(bf: io.BytesIO, v: str, end):
    for c in list(v):
        _uint8(bf, ord(c), end)

def _string(bf: io.BytesIO, v: str, end: str):
    _uint16(bf, len(v), end)
    _nstring(bf, v, end)


@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [FLOAT32_MIN, 1/FLOAT32_MIN, 0, 1/FLOAT32_MAX, FLOAT32_MAX])
def test_float32(v, buffer, endian):
    _float32(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.FLOAT32) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [FLOAT64_MIN, 1/FLOAT64_MIN, 0, 1/FLOAT64_MAX, FLOAT64_MAX])
def test_float64(v, buffer, endian):
    _float64(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.FLOAT64) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [INT8_MIN, 0, INT8_MAX])
def test_int8(v, buffer, endian):
    _int8(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.INT8) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [INT16_MIN, 0, INT16_MAX])
def test_int16(v, buffer, endian):
    _int16(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.INT16) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [INT32_MIN, 0, INT32_MAX])
def test_int32(v, buffer, endian):
    _int32(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.INT32) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [INT64_MIN, 0, INT64_MAX])
def test_int64(v, buffer, endian):
    _int64(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.INT64) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [0, UINT8_MAX])
def test_uint8(v, buffer, endian):
    _uint8(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.UINT8) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [0, UINT16_MAX])
def test_uint16(v, buffer, endian):
    _uint16(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.UINT16) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [0, UINT32_MAX])
def test_uint32(v, buffer, endian):
    _uint32(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.UINT32) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [0, UINT64_MAX])
def test_uint64(v, buffer, endian):
    _uint64(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.bin_read(DTYPES.UINT64) == v


STRING_TEST_VALS = [
    "TestString",
    "Test string with spaces",
    "3",
    "",
    "h"]

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", STRING_TEST_VALS)
def test_string(v, buffer, endian):
    _string(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.string_read() == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", STRING_TEST_VALS)
def test_nstring(v, buffer, endian):
    _nstring(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    assert br.nstring_read(len(v)) == v

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
def test_checkpoint(buffer, endian):
    _nstring(buffer, "a" * 100, endian)
    br = _factory_reader(buffer, endian)
    br.set_checkpoint(50)
    assert br.at_checkpoint() == False
    br.seek(50)
    assert br.at_checkpoint() == True
    br.seek(1)
    assert br.at_checkpoint() == False


def _create_dt(time_millis):
    return datetime.datetime.fromtimestamp(time_millis / 1000, tz=datetime.UTC)

@pytest.mark.parametrize("v", [0, 10, 1000, 10000, 1753265319000, UINT32_MAX])
def test_millis_to_timestamp(v):
    assert BinaryReader.millis_to_timestamp(v) == _create_dt(v)

@pytest.mark.parametrize("endian", ENDIANESS_VALUES)
@pytest.mark.parametrize("v", [
    0, 100, 1000, 10000, 1753265319000
])
def test_timestamp(v, buffer, endian):
    v_dt = _create_dt(v)
    # PyPAMGuard uses millisecond timestamps - remove microsecond accuracy
    _uint64(buffer, v, endian)
    br = _factory_reader(buffer, endian)
    res = br.timestamp_read()
    assert res[0] == v
    assert res[1] == v_dt


def _check_set_bits(bm: Bitmap, tot_bytes: int, exp_val: int):
    """
    Maps the result of get_set_bits() of the Bitmap class on the 
    expected value of set bits.
    """
    assert bm.bits == exp_val
    for i in range(tot_bytes * 4):
        assert ((exp_val >> i) & 1 == 1) if i in bm.get_set_bits() else 1
        assert (i in bm.get_set_bits()) == bm.is_set(i)

def _check_set_bits_with_label(bm: Bitmap, tot_bytes: int, exp_val: int, labels: list[str]):
    assert bm.bits == exp_val
    for i, label in enumerate(labels):
        assert ((exp_val >> i) & 1 == 1) if label in bm.get_set_bits() else 1
        assert (label in bm.get_set_bits()) == bm.is_set(label)


@pytest.mark.parametrize("with_labels", [True, False])
@pytest.mark.parametrize("v", [
    (1, UINT8_MAX),
    (1, 0),
    (1, 1),
    (2, UINT16_MAX),
    (2, 0),
    (2, 1),
    (4, UINT32_MAX),
    (4, 0),
    (4, 1),
    (8, UINT64_MAX),
    (8, 0),
    (8, 1),
    ])
def test_bitmap(v, with_labels):
    if with_labels:
        labels = [str(i) for i in range(v[0] * 8)]
        bm = Bitmap(v[0], labels, v[1])
        _check_set_bits_with_label(bm, v[0], v[1], labels)
    else:
        bm = Bitmap(v[0], None, v[1])
        _check_set_bits(bm, v[0], v[1])

@pytest.mark.parametrize("bytes", range(1, 17))
def test_bitmap_invalid_labels(bytes):
    labels = [str(i) for i in range(bytes * 8)]
    labels.append("Extra")
    with pytest.raises(ValueError):
        Bitmap(bytes, labels, 0)

@pytest.mark.parametrize("s", range(1, 17))
@pytest.mark.parametrize("v", [1.1, 0.3, -10.3, "3"])
def test_bitmap_invalid(s, v):
    with pytest.raises(ValueError):
        Bitmap(s, None, v)

def test_bitmap_invalid_length():
    with pytest.raises(ValueError):
        Bitmap(0, None, 0)
