from abc import ABC, abstractmethod
import numpy as np
import datetime
from pypamguard.utils.bitmap import Bitmap

class Serializable(ABC):
    
    def serialize(self, value):


        if issubclass(type(value), Serializable):
            return value.json()

        def serialize_list(l):
            if isinstance(l, (list, set, np.ndarray)):
                return [serialize_list(i) for i in l]
            elif isinstance(l, np.floating): # remove floating point precision errors#
               return round(float(l), np.finfo(l.dtype).precision)
            elif isinstance(l, np.generic):
                return l.item()
            return l

        if type(value) == np.ndarray or type(value) == list or type(value) == set: return serialize_list(value)
        if type(value) == datetime.datetime: return value.timestamp()
        if type(value) == Bitmap: return value.bits
        if isinstance(value, np.generic): return value.item()

        if isinstance(value, (int, float, str, bool, type(None))): return value
        return str(value)
    

    def to_json(self):
        return {**{attr: self.serialize(value) for attr, value in self.__dict__.items() if not attr.startswith('_')}, "__name__": self.__class__.__name__}

    @classmethod
    def from_json(cls, json):
        raise NotImplementedError
