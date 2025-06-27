from abc import ABC, abstractmethod
import io

class BaseChunk(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def process(self, data: io.BufferedReader):
        if not isinstance(data, io.BufferedReader): raise ValueError(f"data must be of type io.BufferedReader (got {type(data)}).")
 
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
            if not attr.startswith('_'):  # ignore special attributes
                lines.append(f"{attr}: ")
                # Custom code to print the signature of a list
                if isinstance(value, list) and len(value) > 0:
                    shape = []
                    while isinstance(value, list) and len(value) > 0:
                        shape.append(str(len(value)))
                        value = value[0]
                    lines[-1] += f"[{'x'.join(shape)} {value.__class__.__name__}]"
                else:
                    lines[-1] += f"{value}"

        return '\n'.join(lines)