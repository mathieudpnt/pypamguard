from pypamguard.standard import StandardModule, StandardModuleFooter
from pypamguard.core.readers import *


class ClipGenerator(StandardModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)
    
    def _process(self, data, chunk_info):
        pass