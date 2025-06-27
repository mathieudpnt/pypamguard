from .utils.readers import *

def read_beam_former_annotation(self, data):
    self.hydrophones = NumericalBinaryReader(INTS.UINT).process(data)
    self.array_type = NumericalBinaryReader(INTS.SHORT).process(data)
    self.localisation_content = NumericalBinaryReader(INTS.UINT).process(data)
    self.n_angles = NumericalBinaryReader(INTS.SHORT).process(data)
    self.angles = NumericalBinaryReader(FLOATS.FLOAT).process(data, self.n_angles)

def read_bearing_annotation(self, data, annotation_version):
    self.algorithm_name = StringBinaryReader().process(data)
    self.version = annotation_version
    read_beam_former_annotation(self, data)
    self.n_errors = NumericalBinaryReader(INTS.SHORT).process(data)
    self.errors = NumericalBinaryReader(FLOATS.FLOAT).process(data, self.n_errors)
    n_ang = NumericalBinaryReader(INTS.SHORT).process(data)
    self.ref_angles = NumericalBinaryReader(FLOATS.FLOAT).process(data, n_ang)
