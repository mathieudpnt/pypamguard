from modules.headerchunk import HeaderChunk

class PAMFile:
    
    def __init__(self, filename, data, order):
        self.filename = filename
        self.data = data
        self.order = order
        self.current_chunk = None
        self.chunks = []

        self.read_header()

    def read_header(self):
        HeaderChunk(self.data)