# basechunk.py
# Base class for PAMGuard modules

from abc import ABC, abstractmethod
from field import Field
from field_types import *


STRUCTURE = [
    Field("length", IntegerType(INTS.INT)),
    Field("identifier", IntegerType(INTS.INT)),
]


class BaseChunk(ABC):

    @abstractmethod
    def __init__(self, data):
        for field in STRUCTURE:
            setattr(self, field.name, field.process(data))
            print(f"{field.name}: {getattr(self, field.name)}")