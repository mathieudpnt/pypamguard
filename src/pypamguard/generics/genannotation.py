from abc import ABC, abstractmethod

from pypamguard.base import BaseChunk

from .genfileheader import GenericFileHeader
from .genmoduleheader import GenericModuleHeader
from .genmodulefooter import GenericModuleFooter

from pypamguard.core.filters import FILTER_POSITION, Filters
from pypamguard.core.readers import *

class GenericAnnotation(BaseChunk, ABC):
  
    def process(self, br: BinaryReader, *args, **kwargs):
        """
        Pass into kwargs:

        """
        super().process(br, *args, **kwargs)

    def _process(self, br: BinaryReader, *args, **kwargs):
        self.annotation_id = kwargs['annotation_id'] if 'annotation_id' in kwargs else None
        self.annotation_length = kwargs['annotation_length'] if 'annotation_id' in kwargs else None
        self.annotation_version = kwargs['annotation_version'] if 'annotation_version' in kwargs else None
        