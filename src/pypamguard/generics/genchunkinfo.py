from abc import ABC, abstractmethod
import io

from pypamguard.base import BaseChunk

class GenericChunkInfo(BaseChunk, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start: int = None

    @abstractmethod
    def process(self, data: io.BufferedReader):
        raise NotImplementedError()

    @abstractmethod
    def skip(self, data: io.BufferedReader):
        raise NotImplementedError()

    @property
    @abstractmethod
    def next_chunk(self) -> int:
        raise NotImplementedError()
