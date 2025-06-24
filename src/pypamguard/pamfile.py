from readers.structural.fileheader import FileHeader
from readers.structural.moduleheader import ModuleHeader
from readers.structural.header import HeaderChunk
from registry import ModuleRegistry, register_preinstalled_modules
from constants import IdentifierType

class PAMFile:
    
    def __init__(self, filename, data, order):
        self.registry = ModuleRegistry()
        register_preinstalled_modules(self.registry)
        
        self.filename = filename
        self.data = data
        self.order = order
        
        self.current_file_header: FileHeader = None
        self.current_module_header: HeaderChunk = None

        while True:
            self.current_header = HeaderChunk(self.data)
            self.current_header.print()
            
            if self.current_header.identifier == IdentifierType.FILE_HEADER.value:
                self.read_file_header()
            
            elif self.current_header.identifier == IdentifierType.MODULE_HEADER.value:
                self.read_module_header()
            
            elif self.current_header.identifier == 0:
                self.read_data()
            
            else:
                exit()

    def read_data(self):
        self.registry.get_module(self.current_file_header.module_name)(self.data, self.current_file_header, self.current_module_header).print()


    def read_module_header(self):
        self.current_module_header = ModuleHeader(self.data)
        self.current_module_header.print()

    def read_file_header(self):
        self.current_module_header = FileHeader(self.data)
        self.current_file_header = self.current_module_header
        self.current_module_header.print()
