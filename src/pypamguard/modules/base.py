from abc import ABC

class BaseChunk(ABC):

    def  __init__(self):
        self.length = -1
        self.identifier = None