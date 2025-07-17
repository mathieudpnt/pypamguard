from pypamguard.core.serializable import Serializable
from pypamguard.chunks.generics import GenericAnnotation, GenericModule
from pypamguard.core.readers import *

class UserFormAnnotation(GenericAnnotation):

    def _process(self, br: BinaryReader, *args, **kwargs):
        super()._process(br, *args, **kwargs)
        txt_len = self.annotation_length - len(self.annotation_id) - 2 - 2
        self.form_data = br.nstring_read(txt_len)
        