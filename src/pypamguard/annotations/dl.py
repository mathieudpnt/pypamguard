from pypamguard.base.chunk import BaseChunk
from pypamguard.core.serializable import Serializable
from pypamguard.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers import *

class DLAnnotation(GenericAnnotation):

    class ModelData(BaseChunk):
        def _process(self, br: BinaryReader, *args, **kwargs):
            model_type = br.bin_read(DTYPES.INT8)
            is_binary = bool(br.bin_read(DTYPES.INT8) != 0)
            scale = br.bin_read(DTYPES.FLOAT32)
            n_species = br.bin_read(DTYPES.INT16)
            data = br.bin_read((DTYPES.INT16, lambda x: x/scale), shape=(n_species,))

            n_class = br.bin_read(DTYPES.INT16)
            class_names = br.bin_read(DTYPES.INT16, shape=(n_class,))

            if model_type == 0 or model_type == 1: # generic deep learning annotation
                self.predictions = data
                self.class_id = class_names
                self.is_binary = is_binary
                self.type = model_type
            elif model_type == 2: # dummy result
                self.predictions = np.ndarray(0)
                self.type = 'dummy'

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        n_models = br.bin_read(DTYPES.INT16)
        self.models = np.ndarray(n_models, dtype=self.ModelData)
        for i in range(n_models):
            self.models[i] = self.ModelData()
            self.models[i].process(br, *args, **kwargs)
