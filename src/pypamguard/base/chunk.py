from abc import ABC, abstractmethod
import io
from pypamguard.core.serializable import Serializable
from pypamguard.core.readers_new import BinaryReader

class BaseChunk(Serializable, ABC):

    def __init__(self, *args, **kwargs):
        self._measured_length = None

    def _process(self, br: BinaryReader):
        pass

    def process(self, br: BinaryReader, *args, **kwargs):
        start = br.tell()
        self._process(br, *args, **kwargs)
        self._measured_length = br.tell() - start 

    def get_attrs(self):
        return [attr for attr in self.__dict__ if not attr.startswith('_')]

    def signature(self) -> dict:
        lines = {}
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                lines[attr] = type(value)
        return lines

    def __str__(self):
        lines = []
        for attr, value in self.__dict__.items():
            if not attr.startswith('_') and not value is None:
                lines.append(f"{attr} ({type(value)}): ")
                # Custom code to print the signature of a list
                if isinstance(value, list) and len(value) > 0:
                    shape = []
                    while isinstance(value, list) and len(value) > 0:
                        shape.append(str(len(value)))
                        value = value[0]
                    lines[-1] += f"[{'x'.join(shape)} {value.__class__.__name__}]"
                else:
                    lines[-1] += f"{value}"

        return '\t' + '\n\t'.join(lines)
