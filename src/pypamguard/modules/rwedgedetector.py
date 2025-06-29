from ..generics import GenericModule
from ..core.readers import *

class RWEdgeDetector(GenericModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)
    
    def process(self, data, chunk_info):
        pass
