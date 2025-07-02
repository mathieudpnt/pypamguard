from abc import ABC, abstractmethod
import io
import numpy as np
import enum
from pypamguard.logger import logger
import datetime
from pypamguard.utils.bitmap import Bitmap

ENDIANESS = ">"

class DTYPES(enum.Enum):
    INT8 = np.dtype(np.int8).newbyteorder(ENDIANESS)
    UINT8 = np.dtype(np.uint8).newbyteorder(ENDIANESS)
    INT16 = np.dtype(np.int16).newbyteorder(ENDIANESS)
    UINT16 = np.dtype(np.uint16).newbyteorder(ENDIANESS)
    INT32 = np.dtype(np.int32).newbyteorder(ENDIANESS)
    UINT32 = np.dtype(np.uint32).newbyteorder(ENDIANESS)
    INT64 = np.dtype(np.int64).newbyteorder(ENDIANESS)
    UINT64 = np.dtype(np.uint64).newbyteorder(ENDIANESS)
    FLOAT32 = np.dtype(np.float32).newbyteorder(ENDIANESS)
    FLOAT64 = np.dtype(np.float64).newbyteorder(ENDIANESS)

class Shape:
    def __init__(self, shape, length: int):
        self.shape = shape
        self.length = length
        
        if type(self.shape) == self.__class__:
            self.size = self.length * self.shape.size
        elif type(self.shape) == DTYPES:
            self.size = self.length * self.shape.value.itemsize
            self.shape = self.shape.value
        else:
            raise ValueError(f"shape must be of type Shape or np.dtype (got {type(self.shape)}).")

    def __str__(self):
        if type(self.shape) == self.__class__:
            return f"{self.length} * ({self.shape})"
        else:
            return f"{self.length} * {self.shape}"

class BinaryReader:
    def __init__(self, fp: io.BufferedReader):
        self.fp = fp

    def __collate(self, data, dtypes, shape):
        for i, dtype_i in enumerate(dtypes):
            d = data[f'f{i}'][0] if (len(shape) == 1 and shape[0] == 1) else data[f'f{i}'].reshape(shape)
            yield dtype_i[1](d) if dtype_i[1] is not None else d

    def read_numeric(self, dtype: DTYPES | list[DTYPES], shape: tuple = (1,)) -> int | float | np.ndarray | tuple[np.ndarray]:
        """
        Read numeric data from the file. This function is polymorphic in the sense that it
        can be used for any of the following purposes:

        1. Read in a single value of a given datatype (for example `read_numeric(DTYPES.INT32)`).
        2. Read in an array of values of a given datatype (for example `read_numeric(DTYPES.INT32, (5,))`).
        3. Read in an n-dimensional array of values of a given datatype (for example `read_numeric(DTYPES.INT32, (5, 5))`).
        4. Read in an interleaved array of values of a given datatype (for example `read_numeric([DTYPES.INT32, DTYPES.INT32], (5,))`).

        """

        dtypes = [(dtype_i, None) if isinstance(dtype_i, DTYPES) else dtype_i for dtype_i in ([dtype] if not isinstance(dtype, list) else dtype)]
        data_length = sum(dtype_i[0].value.itemsize for dtype_i in dtypes) * np.prod(shape)   
        data = np.frombuffer(self.fp.read(data_length), dtype=[(f'f{i}', dtype_i[0].value) for i, dtype_i in enumerate(dtypes)])
        ret_val = tuple(self.__collate(data, dtypes, shape))
        return ret_val[0] if len(ret_val) == 1 else ret_val

    def read_timestamp(self) -> tuple[int, datetime.datetime]:
        timestamp = self.read_numeric(DTYPES.INT64)
        return timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=datetime.UTC)

    def read_nstring(self, length: int) -> str:
        return self.fp.read(length).decode("utf-8")

    def read_string(self) -> str:
        return self.read_nstring(self.read_numeric(DTYPES.INT16))
    
    def read_bitmap(self, dtype: DTYPES, labels: list[str] = None) -> Bitmap:
        return Bitmap(dtype.value.itemsize, labels, int(self.read_numeric(dtype)))