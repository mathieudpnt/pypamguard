# basechunk.py
# Base class for PAMGuard modules

from abc import ABC

class BaseChunk(ABC):

    def __init__(self, data):
        pass
    
    def print(self):
        for attr, value in self.__dict__.items():
            if not attr.startswith('__'):  # ignore special attributes
                print(f"{attr}: {value}")
